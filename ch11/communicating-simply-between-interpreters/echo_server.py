#!/usr/bin/env python
import traceback
from multiprocessing.connection import Listener


def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print("connection closed")


def echo_server(addr, authkey):
    server = Listener(addr, authkey=authkey)
    while True:
        try:
            client = server.accept()
            echo_client(client)
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    echo_server(("", 25000), authkey=b"peekaboo")
