#!/usr/bin/env python
import socket
from functools import partial


def echo_handler(addr: str, client_sock: socket.socket):
    print("got connection from:", addr)
    for msg in iter(partial(client_sock.recv, 8192), b""):
        client_sock.sendall(msg)

    client_sock.close()


def echo_server(addr: str, backlog: int = 5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)


if __name__ == "__main__":
    echo_server(("", 20000))
