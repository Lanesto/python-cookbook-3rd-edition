#!/usr/bin/env python
import getpass


def login(user, passwd):
    if user == "root":
        return passwd == "1234"


user = getpass.getuser()
passwd = getpass.getpass()

if login(user, passwd):
    print("ok")
else:
    print("invalid")
