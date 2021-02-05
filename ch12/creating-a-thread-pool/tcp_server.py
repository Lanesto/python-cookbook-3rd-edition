#!/usr/bin/env python
import socket
from concurrent.futures import ThreadPoolExecutor
from functools import partial


def echo_handler(sock, client_addr):
    print("got connection from", client_addr)
    for msg in iter(partial(sock.recv, 8192), b""):
        sock.sendall(msg)

    print("closing connection", client_addr)


def echo_server(addr):
    with ThreadPoolExecutor(128) as pool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        sock.listen(5)
        while True:
            client_sock, client_addr = sock.accept()
            pool.submit(echo_handler, client_sock, client_addr)


if __name__ == "__main__":
    echo_server(("", 15000))
