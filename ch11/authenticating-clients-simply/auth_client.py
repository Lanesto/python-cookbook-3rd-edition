#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_STREAM
from auth_helper import client_authenticate

secret_key = b"peekaboo"


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 18000))
    client_authenticate(s, secret_key)
    s.send(b"Hello World")
    resp = s.recv(8192)
    print(resp)