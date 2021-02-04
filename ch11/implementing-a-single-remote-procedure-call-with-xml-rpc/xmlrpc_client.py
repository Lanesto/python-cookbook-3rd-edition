#!/usr/bin/env python
from xmlrpc.client import ServerProxy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    s = ServerProxy("http://localhost:15000", allow_none=True)
    s.set("foo", "bar")
    s.set("spam", [1, 2, 3])
    print(s.keys())
    print(s.get("spam"))
    s.delete("spam")
    print(s.exists("spam"))
    s.set("foo", Point(2, 3))
    print(s.get("foo"))
    s.set("bar", b"Hello World")
    print(repr(s.get("bar")))
