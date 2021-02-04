#!/usr/bin/env python
import ssl
from socket import socket, AF_INET, SOCK_STREAM


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s = ssl.wrap_socket(
        s, cert_reqs=ssl.CERT_REQUIRED, ca_certs="server_cert.pem"
    )
    s.connect(("localhost", 20000))
    s.send(b"Hello World?")
    print(s.recv(8192))
