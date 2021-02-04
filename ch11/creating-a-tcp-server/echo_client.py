#!/usr/bin/env python
import socket


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 20000))
    s.send(b"hello\n")
    msg = s.recv(8192)
    print(msg)
