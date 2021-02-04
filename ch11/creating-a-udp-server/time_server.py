#!/usr/bin/env python
from socketserver import BaseRequestHandler, ThreadingUDPServer
import time


class TimeHandler(BaseRequestHandler):
    def handle(self):
        print("got connection from", self.client_address)
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode("ascii"), self.client_address)


if __name__ == "__main__":
    server = ThreadingUDPServer(("", 20000), TimeHandler)
    server.serve_forever()
