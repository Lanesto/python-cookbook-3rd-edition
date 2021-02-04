#!/usr/bin/env python
import time
from socket import socket, AF_INET, SOCK_DGRAM


def time_server(addr):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(addr)
    while True:
        msg, addr = sock.recvfrom(8192)
        print("got message from", addr)
        resp = time.ctime()
        sock.sendto(resp.encode("ascii"), addr)


if __name__ == "__main__":
    time_server(("", 20000))
