#!/usr/bin/python
# coding: utf-8
__author__ = 'lhfcws'

import sys, os
import getpass
from scripts.yah3c_core import *

# Constants
STOP = "stop"
START = "start"
LOCAL_CONFIG_PATH = "~/.yah3c/"


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


def start_conf():
    username = raw_input("Enter your netID: ")
    passwd = getpass.getpass("Enter your netID password: ")
    passwd1 = getpass.getpass("Enter your netID password again: ")
    if passwd != passwd1:
        display_info("Error: You've input different passwords!")
        return
    device = raw_input("Enter your ethernet device (default en4): ")

    save_conf(username, passwd, device)
    return (username, passwd, device)


def start():
    init()

    args = sys.argv[1:]
    if len(args) == 0 or args[0] == START:
        conf = load_conf()
        if not conf:
            conf = start_conf()

        connect(*conf)
    elif args[0] == STOP:
        os.system("ps -ef | grep 'yah3c.py' | grep '^grep' | awk '{split($0,a);print a[2];}'")
        sysout = os.popen("ps -ef | grep 'yah3c.py' | grep '^grep' | awk '{split($0,a);print a[2];}'")
        for process_id in sysout:
            os.system("kill " + process_id)
            display_info("Kill YaH3C, process id is " + process_id)
            break   # always kill the first 1



if __name__ == "__main__":
    start()

