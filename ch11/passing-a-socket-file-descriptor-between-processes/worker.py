#!/usr/bin/env python
import socket
import struct
from functools import partial


def recv_fd(sock):
    msg, ancdata, flags, addr = sock.recvmsg(
        1, socket.CMSG_LEN(struct.calcsize("i"))
    )
    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS
    sock.sendall(b"OK")


def worker(server_addr):
    serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    serv.connect(server_addr)
    while True:
        fd = recv_fd(serv)
        print("worker: got fd", fd)
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, fileno=fd
        ) as client:
            for msg in iter(partial(client.recv, 1024), b""):
                print(f"worker: recv {msg!r}")
                client.send(msg)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} server_addr".format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])
