#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer


class KeyValueServer:
    _rpc_methods = ["get", "set", "delete", "exists", "keys"]

    def __init__(self, addr):
        self._data = {}
        self._server = SimpleXMLRPCServer(addr, allow_none=True)
        for name in self._rpc_methods:
            self._server.register_function(getattr(self, name))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._server.serve_forever()


if __name__ == "__main__":
    kv_server = KeyValueServer(("", 15000))
    kv_server.serve_forever()
