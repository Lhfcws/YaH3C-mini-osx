#!/usr/bin/python
# coding: utf-8

import sys, os
import pcap

from struct import pack, unpack

## Constants
# Reference: http://tools.ietf.org/html/rfc3748
ETHERTYPE_PAE = 0x888e
PAE_GROUP_ADDR = "\x01\x80\xc2\x00\x00\x03"
BROADCAST_ADDR = "\xff\xff\xff\xff\xff\xff"
VERSION_INFO = "\x06\x07bjQ7SE8BZ3MqHhs3clMregcDY3Y=\x20\x20"

EAPOL_VERSION = 1
EAPOL_EAPPACKET = 0

# packet info for EAPOL_EAPPACKET
EAPOL_START = 1
EAPOL_LOGOFF = 2
EAPOL_KEY = 3
EAPOL_ASF = 4

EAP_REQUEST = 1
EAP_RESPONSE = 2
EAP_SUCCESS = 3
EAP_FAILURE = 4

# packet info followed by EAP_RESPONSE
# 1       Identity
# 2       Notification
# 3       Nak (Response only)
# 4       MD5-Challenge
# 5       One Time Password (OTP)
# 6       Generic Token Card (GTC)
# 254     Expanded Types
# 255     Experimental use
EAP_TYPE_ID = 1  # identity
EAP_TYPE_NOTIFICATION = 2  # Notification
EAP_TYPE_MD5 = 4  # md5 Challenge
EAP_TYPE_H3C = 7  # H3C eap packet(used for SYSU east campus)


def mac_repr(mac):
    return ':'.join(['%02x'] * 6) % tuple(map(ord, mac))


def md5_repr(md5hash):
    return ':'.join('%02x' % ord(x) for x in md5hash)


EAPOL_TYPE_MAP = {
    EAPOL_EAPPACKET: 'EAPOL_EAPPACKET',
    EAPOL_VERSION: 'EAPOL_VERSION',
}

EAP_CODE_MAP = {
    EAP_REQUEST: 'EAP_REQUEST',
    EAP_RESPONSE: 'EAP_RESPONSE',
    EAP_SUCCESS: 'EAP_SUCCESS',
    EAP_FAILURE: 'EAP_FAILURE',
}


def parse_header(ethernetHeader):
    # header: 6(dest mac)|6(src mac)|2(type)
    return ethernetHeader[:6], ethernetHeader[6:12], unpack('!H', ethernetHeader[12:14])[0]


def dump(packet, f=open('/tmp/packetsdump', 'a'), split='>'):
    f.write(split * 80)
    f.write('\n')
    header, packet = packet[:14], packet[14:]
    headerRepr = 'dst:%s|src:%s|typ:0x%x|\n' % (
        mac_repr(header[:6]), mac_repr(header[6:12]), unpack('!H', header[12:14])[0])
    f.write(headerRepr)
    # body, meta info
    verson, type, eapolLen = unpack("!BBH", packet[:4])
    bodyRepr = 'ver:%d|typ2:%d(%s)|eapollen:%d|\n' % (
        verson, type, EAPOL_TYPE_MAP.get(type, 'unknown'), eapolLen)
    f.write(bodyRepr)
    if type != EAPOL_EAPPACKET:
        # meet unknown type, dump all rest data.
        f.write(packet[4:8])
    else:
        # parse payload
        code, id, eapLen = unpack("!BBH", packet[4:8])
        eapRepr = 'code:%d(%s)|id:%d|eaplen:%d|\n' % (
            code, EAP_CODE_MAP.get(code, 'unknown'), id, eapLen)
        f.write(eapRepr)
        if code == EAP_REQUEST or code == EAP_RESPONSE:
            reqType = unpack("!B", packet[8:9])[0]
            reqData = packet[9: 4 + eapLen]
            if reqType == EAP_TYPE_ID:
                f.write('reqtype:identity|ver+username:%s|' % (reqData))
            elif reqType == EAP_TYPE_H3C:
                # TODO: not implemented
                pass
            elif reqType == EAP_TYPE_MD5:
                chapLen = unpack('!B', reqData[0:1])[0]
                f.write('reqtype:md5|chap(%d):%s|username:%s|' % (
                    chapLen, md5_repr(reqData[1:chapLen + 1]), reqData[chapLen + 1:]))
            else:
                f.write('reqtype:%d(unknown)|%s|' % (reqType, reqData))
        else:
            f.write('%s|' % packet[8:])

    f.write('\n')
    f.flush()


def make_ethernet_header(src, dst, type):
    return dst + src + pack("!H", type)


def make_EAPOL(type, payload=""):
    return pack("!BBH", EAPOL_VERSION, type, len(payload)) + payload


def make_EAP(code, id, type=0, data=""):
    if code in [EAP_SUCCESS, EAP_FAILURE]:
        return pack("!BBH", code, id, 4)
    else:
        return pack("!BBHB", code, id, 5 + len(data), type) + data


def display_info(s):
    print s


def display_response_info(s):
    try:
        display_info('>> ' + s.decode('gbk'))
    except:
        display_info('>> ' + s)


EMPTY_IP = (0, 0, 0, 0)


def get_ipaddr_slow(device):
    try:
        path = "/tmp/_asdfafip"
        os.system("ip address show dev %s >%s" % (device, path))
        data = open(path, 'r').read().split()
        return tuple(map(int, data[data.index('inet') + 1].split('/')[0].split('.')))
    except:
        return EMPTY_IP


def get_ipaddr(device):
    try:
        import commands

        data = commands.getoutput('ip address show dev ' + device)
        return tuple(map(int, data[data.index('inet') + 1].split('/')[0].split('.')))
    except:
        return get_ipaddr_slow(device)


def get_mac_addr(device):
    def pack_mac(mac_addrs):
        args = []
        for hex_item in mac_addrs:
            args.append(int("0x" + hex_item, 16))
        return pack("!BBBBBB", *args)

    is_this_device = False
    for line in os.popen("ifconfig"):
        if is_this_device and line.find("ether") >= 0:
            lines = line.split()
            for item in lines:
                if item.count(":") == 5:
                    return pack_mac(item.split(":"))

        if line.strip().startswith(device):
            is_this_device = True


def connect(username, password, device, login=True):
    client = pcap.pcap(name=device, timeout_ms=15000, snaplen=65535, immediate=True)

    macAddr = get_mac_addr(device)
    ethernetHeader = make_ethernet_header(macAddr, PAE_GROUP_ADDR, ETHERTYPE_PAE)
    hasSentLogoff = False
    # ip = EMPTY_IP

    class Status(object):
        def __init__(self):
            self.serverMac = None
            self.success = False

    def send(data):
        client.sendpacket(data)
        dump(data, split='<')

    def send_response_id(packetID):
        ip = get_ipaddr(device)
        # magic1 = '\xc2'
        # magic2 = '\xa3'
        response = '\x15\x04' + pack('!BBBB', *ip) + VERSION_INFO + username
        send(ethernetHeader + make_EAPOL(EAPOL_EAPPACKET,
                                         make_EAP(EAP_RESPONSE, packetID, EAP_TYPE_ID, response)))

    def send_response_h3c(packetID):
        response = chr(len(password)) + password + username
        eapPacket = ethernetHeader + make_EAPOL(EAPOL_EAPPACKET,
                                                make_EAP(EAP_RESPONSE, packetID, EAP_TYPE_H3C, response))
        send(eapPacket)

    def send_response_md5(packetID, md5data):
        md5 = password[0:16] + '\x00' * (16 - len(password))
        chap = ''.join(chr(ord(md5[i]) ^ ord(md5data[i])) for i in xrange(16))
        response = pack('!B', len(chap)) + chap + username
        send(ethernetHeader + make_EAPOL(EAPOL_EAPPACKET, make_EAP(
            EAP_RESPONSE, packetID, EAP_TYPE_MD5, response)))

    def send_start():
        send(ethernetHeader + make_EAPOL(EAPOL_START))
        display_info('Sending EAPOL start...')

    def send_logoff():
        display_info('Sending EAPOL logoff...')
        send(ethernetHeader + make_EAPOL(EAPOL_LOGOFF))
        hasSentLogoff = True


    def on_receive(timestamp, packet):
        # print "# recv: " + packet
        eapPacket = packet
        rawPacket = eapPacket
        header, eapPacket = eapPacket[:14], eapPacket[14:]
        dstMac, srcMac, _ = parse_header(header)
        if dstMac != macAddr:
            return
        dump(rawPacket)

        if status.serverMac is None:
            display_info("Waiting a few seconds please ~~")
            status.serverMac = srcMac
            ethernetHeader = make_ethernet_header(macAddr, status.serverMac, ETHERTYPE_PAE)

        vers, type, eapolLen = unpack("!BBH", eapPacket[:4])
        if type == EAPOL_EAPPACKET:
            code, id, eapLen = unpack("!BBH", eapPacket[4:8])
            if code == EAP_SUCCESS:
                display_info('Got EAP Success. Check it out in your browser and enjoy your network.')
                if not status.success:
                    daemonize(stdout='/tmp/yah3c.out.log', stderr='/tmp/yah3c.err.log')
                status.success = True
            elif code == EAP_FAILURE:
                if hasSentLogoff:
                    display_info('Logoff Successfully.')
                else:
                    display_info('Got EAP Failure')
                display_response_info(eapPacket[10:])
            elif code == EAP_REQUEST:
                reqType = unpack("!B", eapPacket[8:9])[0]
                reqData = eapPacket[9: 4 + eapLen]
                if reqType == EAP_TYPE_ID:
                    display_info('Get EAP Request for identity.')
                    send_response_id(id)
                    display_info('Sending EAP response with identity = [%s]' % username)
                elif reqType == EAP_TYPE_H3C:
                    display_info('Got EAP Request for Allocation.')
                    send_response_h3c(id)
                    display_info('Sending EAP response with password...')
                elif reqType == EAP_TYPE_MD5:
                    dataLen = unpack("!B", reqData[0:1])[0]
                    md5data = reqData[1:1 + dataLen]
                    display_info('Get EAP Request for MD5-Challenge')
                    send_response_md5(id, md5data)
                    display_info('Sending EAP response with password...')
                else:
                    display_info('Got unknown request type %i' % reqType)
            elif code == 10:
                display_response_info(eapPacket[12:])
            elif code == EAP_RESPONSE:
                dump(rawPacket, sys.stdout)
                # display_info('Got Unknown EAP Response')
            else:
                pass
                #display_info('Got unknown EAP code (%i)' % code)
        else:
            display_info('Got unknown EAPOL type %i' % type)

    if not login:
        send_logoff()
        return

    try:
        print "Begin Authentication"
        status = Status()
        send_start()
        client.loop(0, on_receive)
        print "End Authentication"
    except Exception, e:
        display_info('Connection error: ' + str(e))
        exit(-1)
    finally:
        if status.success:
            send_logoff()


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''This forks the current process into a daemon. The stdin, stdout, and
    stderr arguments are file names that will be opened and be used to replace
    the standard file descriptors in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null. Note that stderr is
    opened unbuffered, so if it shares a file with stdout then interleaved
    output may not appear in the order that you expect. '''

    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    device = sys.argv[3] if len(sys.argv) > 3 else 'en0'
    connect(username, password, device)
