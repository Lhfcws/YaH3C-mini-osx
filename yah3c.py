#!/usr/bin/python
# coding: utf-8
__author__ = 'lhfcws'

import getpass
import os
import sys
from scripts.yah3c_core import *

##############################
# Constants
NEW = "new"
HELP = "help"
LIST = "list"
STOP = "stop"
START = "start"
RESTART = "restart"
LOCAL_CONFIG_PATH = os.path.abspath("/etc/yah3c/")
LOCAL_USER_CONFIG_PATH = LOCAL_CONFIG_PATH + "users/"
LOCAL_DEFAULT_USER_CONFIG_PATH = LOCAL_USER_CONFIG_PATH + "default_user"
CMD_STOP = "ps -ef | grep 'yah3c.py' | grep -v 'grep' |\
           awk '{split($0,a);print a[2];}'"
##############################


class ConfUtil(object):
    """
    Encapsulation of local methods
    """

    @staticmethod
    def init():
        os.system("mkdir -p " + LOCAL_USER_CONFIG_PATH)

    @staticmethod
    def load_conf():
        try:
            user = ConfUtil.get_default_user()
            if not user:
                return None
            fp = open(LOCAL_USER_CONFIG_PATH + user, "r")
            username = fp.readline().strip()
            password = fp.readline().strip()
            device = fp.readline().strip()
            fp.close()
            return (username, password, device)
        except Exception:
            return None

    @staticmethod
    def save_conf(username, password, device):
        fp = open(LOCAL_USER_CONFIG_PATH + username, "w")
        fp.write(username + "\n")
        fp.write(password + "\n")
        fp.write(device)
        fp.close()

        display_info("Save user information to local disk.")

    @staticmethod
    def delete_conf(user):
        try:
            os.remove(LOCAL_USER_CONFIG_PATH + user)
            return True
        except IOError:
            return False

    @staticmethod
    def new_conf():
        username = raw_input("Enter your netID: ")
        passwd = getpass.getpass("Enter your netID password: ")
        passwd1 = getpass.getpass("Enter your netID password again: ")
        if passwd != passwd1:
            display_info("Error: You've input different passwords!")
            exit(-1)
        device = raw_input("Enter your ethernet device (see in ifconfi): ")

        ConfUtil.save_conf(username, passwd, device)
        return (username, passwd, device)

    @staticmethod
    def set_default_user(username):
        fp = open(LOCAL_DEFAULT_USER_CONFIG_PATH, "w")
        fp.write(username)
        fp.close()

    @staticmethod
    def get_default_user():
        try:
            fp = open(LOCAL_DEFAULT_USER_CONFIG_PATH, "r")
            username = fp.readline()
            fp.close()
            return username
        except IOError:
            return None

    @staticmethod
    def get_user_list():
        return os.listdir(LOCAL_USER_CONFIG_PATH)

    @staticmethod
    def print_cmd_help():
        print "Usage of YaH3C-mini-osx (you should use it under 'sudo') : "
        print "  sudo python yah3c.py (start)       - Start yah3c."
        print "  sudo python yah3c.py new           - Start yah3c with new user."
        print "  sudo python yah3c.py stop          - Stop yah3c."
        print "  sudo python yah3c.py restart       - Restart yah3c (stop & start)."
        print "  python yah3c.py list               - List the running yah3c process."
        print "  python yah3c.py help               - Print this help message."


class Yah3cApi(object):
    """ Api Wrapper class.
    You can refer to this class if you wanna add a shell for YaH3C-mini-osx.
    """

    def __init__(self):
        ConfUtil.init()

    def list_process(self):
        """ Show and return current running yah3c processes.
        :return: list [pid]
        """
        cmd = "ps -ef | grep 'yah3c' | grep -v 'grep' | grep -v 'list'"
        has_process = False
        processes = []

        sysout = os.popen(cmd)
        for process in sysout:
            print process
            has_process = True
            processes.append(process)

        if not has_process:
            print "There is no yah3c process running now."

        sysout.close()
        return processes

    def list_user(self):
        """ Show and return the configed users.
        :return: list [username]
        """
        users = ConfUtil.get_user_list()
        for user in users:
            print user
        return users

    def delete_user(self, username):
        """ Delete a user config.
        :return: bool Success flag
        """
        return ConfUtil.delete_conf(username)

    def stop(self):
        """ Short method of stop(cmd). Stop all the yah3c related processes.
        :return: list [stopped_pid]
        """
        return self.stop(CMD_STOP)

    def stop(self, cmd):
        """ Stop all the yah3c related processes.
        :param cmd: shell command of stopping yah3c
        :return: list [stopped_pid]
        """
        my_pid = os.getpid()
        my_ppid = os.getppid()
        pids = []

        sysout = os.popen(cmd)
        for process_id in sysout:
            if str(my_pid) == process_id.strip() or str(my_ppid) == process_id.strip():
                continue

            pids.append(process_id)
            os.system("sudo kill " + process_id)
            display_info("Kill YaH3C, process id is " + process_id)

        sysout.close()
        return pids

    def start(self):
        conf = ConfUtil.load_conf()
        if not conf:
            conf = ConfUtil.new_conf()

        connect(*conf)

    def restart(self):
        import time

        try:
            self.stop()
        except Exception:
            print "Skip stopping yah3c."
        finally:
            time.sleep(1)
            display_info("Restarting yah3c...")
            self.start()

    def start_user(self, new_user):
        # Verify the user's existion
        users = ConfUtil.get_user_list()
        if users.count(new_user) <= 0:
            return None

        ConfUtil.set_default_user(new_user)
        self.restart()


#################################
if __name__ == "__main__":
    def main():
        api = Yah3cApi()

        args = sys.argv[1:]
        if len(args) > 1:
            display_info("Too many arguments.")
            return

        if len(args) == 0 or args[0] == START:
            api.start()
        elif args[0] == NEW:
            conf = ConfUtil.new_conf()
            connect(*conf)
        elif args[0] == STOP:
            api.stop()
        elif args[0] == RESTART:
            api.restart()
        elif args[0] == LIST:
            api.list_process()
        else:
            ConfUtil.print_cmd_help()
    ################################
    main()

