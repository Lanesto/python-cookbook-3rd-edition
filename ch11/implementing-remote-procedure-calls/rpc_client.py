#!/usr/bin/env python
import pickle
from multiprocessing.connection import Client


class RPCProxy:
    def __init__(self, conn):
        self._conn = conn

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._conn.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._conn.recv())
            if isinstance(result, Exception):
                raise Exception

            return result

        return do_rpc


if __name__ == "__main__":
    c = Client(("localhost", 17000), authkey=b"peekaboo")
    proxy = RPCProxy(c)
    print(proxy.add(2, 3))
    print(proxy.sub(2, 3))
    print(proxy.sub([1, 2], 4))
