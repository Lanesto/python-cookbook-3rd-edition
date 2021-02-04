#!/usr/bin/env python
from multiprocessing.connection import Client


if __name__ == "__main__":
    c = Client(("localhost", 25000), authkey=b"peekaboo")
    c.send("hello")
    print(c.recv())
    c.send([1, 2, 3, 4, 5])
    print(c.recv())
    c.close()
