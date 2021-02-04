#!/usr/bin/env python
import pickle
from multiprocessing.connection import Listener
from threading import Thread


class RPCHandler:
    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                func_name, args, kwargs = pickle.loads(connection.recv())
                try:
                    result = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(result))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass


def rpc_server(handler, addr, authkey):
    sock = Listener(addr, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(
            target=handler.handle_connection, args=(client,), daemon=True
        )
        t.start()


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)


if __name__ == "__main__":
    rpc_server(handler, ("localhost", 17000), authkey=b"peekaboo")
