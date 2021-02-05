#!/usr/bin/env python
import socket
from threading import Thread
from queue import Queue
from functools import partial


def echo_handler(q):
    sock, c_addr = q.get()
    print("got connection from", c_addr)
    for msg in iter(partial(sock.recv, 65536), b""):
        sock.sendall(msg)

    print("closed connection", c_addr)
    sock.close()


def echo_server(addr, num_workers):
    q = Queue()
    for i in range(num_workers):
        t = Thread(target=echo_handler, args=(q,), daemon=True)
        t.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        q.put((client_sock, client_addr))


if __name__ == "__main__":
    echo_server(("", 15000), 32)
