#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_STREAM
from auth_helper import server_authenticate

secret_key = b"peekaboo"


def echo_handler(client_sock):
    if not server_authenticate(client_sock, secret_key):
        client_sock.close()
        return

    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)


def echo_server(addr):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(addr)
    s.listen(5)
    while True:
        conn, addr = s.accept()
        echo_handler(conn)


if __name__ == "__main__":
    echo_server(("", 18000))
