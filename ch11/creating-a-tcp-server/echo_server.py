#!/usr/bin/env python
import threading
from socketserver import StreamRequestHandler, TCPServer
import socket

NUM_WORKERS = 16


class EchoHandler(StreamRequestHandler):
    timeout = 5
    rbufsize = -1
    wbufsize = 0
    disable_nagle_algorithm = False

    def handle(self):
        print("got connection from:", self.client_address)
        try:
            for line in self.rfile:
                self.wfile.write(line)
        except socket.timeout:
            print("timed out for connection:", self.client_address)


if __name__ == "__main__":
    server = TCPServer(("", 20000), EchoHandler, bind_and_activate=False)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server.server_bind()
    server.server_activate()
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

    server.serve_forever()
