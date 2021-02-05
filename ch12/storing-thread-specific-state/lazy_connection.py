#!/usr/bin/env python
import threading
import socket
from functools import partial


class LazyConnection:
    def __init__(self, addr, family=socket.AF_INET, type=socket.SOCK_STREAM):
        self.addr = addr
        self.family = family
        self.type = type
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, "sock"):
            raise RuntimeError("already connected")
        self.local.sock = socket.socket(self.family, self.type)
        self.local.sock.connect(self.addr)
        return self.local.sock

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.local.sock.close()
        del self.local.sock


def test(conn):
    with conn as s:
        s.send(b"GET /index.html HTTP/1.0\r\n")
        s.send(b"Host: www.python.org\r\n")
        s.send(b"\r\n")
        resp = b"".join(iter(partial(s.recv, 8192), b""))

    print("got {} bytes".format(len(resp)))


if __name__ == "__main__":
    conn = LazyConnection(("www.python.org", 80))
    t1 = threading.Thread(target=test, args=(conn,))
    t2 = threading.Thread(target=test, args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
