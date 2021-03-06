#!/usr/bin/env python
import socket
import struct


def send_fd(sock, fd):
    sock.sendmsg(
        [b"x"], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack("i", fd))]
    )
    ack = sock.recv(2)
    assert ack == b"OK"


def server(work_addr, port):
    work_serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    work_serv.bind(work_addr)
    work_serv.listen(1)
    worker, addr = work_serv.accept()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(("", port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print("server: got connection from", addr)
        send_fd(worker, client.fileno())
        client.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(
            "usage: {} server_addr server_port".format(sys.argv[0]),
            file=sys.stderr,
        )
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))
