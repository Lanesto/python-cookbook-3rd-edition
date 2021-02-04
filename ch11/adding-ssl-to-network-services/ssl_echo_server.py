#!/usr/bin/env python
import ssl
from socket import socket, AF_INET, SOCK_STREAM

KEY_FILE = "server_key.pem"
CERT_FILE = "server_cert.pem"


def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b"":
            break
        s.send(data)
    s.close()
    print("connection closed")


def echo_server(addr):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(addr)
    s.listen(1)
    s = ssl.wrap_socket(
        s, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True
    )
    while True:
        try:
            c, a = s.accept()
            print("got connection:", c, a)
            echo_client(c)
        except Exception as e:
            print("{}: {}".format(e.__class__.__name__, e))


if __name__ == "__main__":
    echo_server(("", 20000))
