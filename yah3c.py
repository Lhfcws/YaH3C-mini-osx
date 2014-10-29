#!/usr/bin/python
# coding: utf-8
__author__ = 'lhfcws'

import sys, os
import getpass
from scripts.yah3c_core import *

# Constants
NEW = "new"
HELP = "help"
LIST = "list"
STOP = "stop"
START = "start"
RESTART = "restart"
LOCAL_CONFIG_PATH = os.path.abspath("/etc/yah3c/")


def init():
    os.system("mkdir -p " + LOCAL_CONFIG_PATH)


def load_conf():
    try:
        fp = open(LOCAL_CONFIG_PATH + "yah3c_user.conf", "r")
        username = fp.readline().strip()
        password = fp.readline().strip()
        device = fp.readline().strip()
        fp.close()
        return (username, password, device)
    except Exception:
        return None


def save_conf(username, password, device):
    fp = open(LOCAL_CONFIG_PATH + "yah3c_user.conf", "w")
    fp.write(username + "\n")
    fp.write(password + "\n")
    fp.write(device)
    fp.close()

    display_info("Save user information to local disk.")


def start_conf():
    username = raw_input("Enter your netID: ")
    passwd = getpass.getpass("Enter your netID password: ")
    passwd1 = getpass.getpass("Enter your netID password again: ")
    if passwd != passwd1:
        display_info("Error: You've input different passwords!")
        exit(-1)
    device = raw_input("Enter your ethernet device (see in ifconfi): ")

    save_conf(username, passwd, device)
    return (username, passwd, device)


def print_help():
    print "Usage of YaH3C-mini-osx (you should use it under 'sudo') : "
    print "  sudo python yah3c.py (start)       - Start yah3c."
    print "  sudo python yah3c.py new           - Start yah3c with new user."
    print "  sudo python yah3c.py stop          - Stop yah3c."
    #print "  sudo python yah3c.py restart       - Restart yah3c (stop & start)."
    print " python yah3c.py list                - List the running yah3c process."
    print "  python yah3c.py help               - Print this help message."


def start():
    cmd_stop = "ps -ef | grep 'yah3c.py' | grep -v 'grep' | grep -v 'stop' |\
            awk '{split($0,a);print a[2];}'"

    cmd_restart_stop = "ps -ef | grep 'yah3c.py' | grep -v 'grep' | grep -v 'restart' |\
            awk '{split($0,a);print a[2];}'"

    def _list():
        cmd = "ps -ef | grep 'yah3c' | grep -v 'grep' | grep -v 'list'"
        has_process = False

        sysout = os.popen(cmd)
        for process in sysout:
            print process
            has_process = True

        if not has_process:
            print "There is no yah3c process running now."

        sysout.close()

    def _stop(cmd):
        '''
        my_pid = os.getpid()
        sysout = os.popen("ps -ef | grep 'python yah3c.py$' | awk '{split($0,a);print a[2];}'")
        for process_id in sysout:
            if int(process_id) == my_pid:
                continue
            os.system("kill " + process_id)
            display_info("Kill YaH3C, process id is " + process_id)
        sysout.close()
        '''

        sysout = os.popen(cmd)
        for process_id in sysout:
            os.system("sudo kill " + process_id)
            display_info("Kill YaH3C, process id is " + process_id)
        sysout.close()


    def _start():
        conf = load_conf()
        if not conf:
            conf = start_conf()

        connect(*conf)

    def _restart():
        import time

        try:
            _stop(cmd_restart_stop)
        except Exception:
            print "Skip stopping yah3c."
        finally:
            time.sleep(1)
            display_info("Restarting yah3c...")
            _start()


    init()

    args = sys.argv[1:]
    if len(args) > 1:
        display_info("Too many arguments.")
        return

    if len(args) == 0 or args[0] == START:
        _start()
    elif args[0] == NEW:
        conf = start_conf()
        connect(*conf)
    elif args[0] == STOP:
        _stop(cmd_stop)
    elif args[0] == RESTART:
        _restart()
    elif args[0] == LIST:
        _list()
    else:
        print_help()



if __name__ == "__main__":
    start()

