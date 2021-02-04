#!/usr/bin/env python
import os
from multiprocessing.connection import Client
from multiprocessing.reduction import recv_handle
from socket import socket, AF_INET, SOCK_STREAM


def worker(server_addr):
    server = Client(server_addr, authkey=b"peekaboo")
    server.send(os.getpid())
    while True:
        fd = recv_handle(server)
        print("worker: got fd", fd)
        with socket(AF_INET, SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print(f"worker: recv {msg!r}")
                client.send(msg)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} server_addr".format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])
