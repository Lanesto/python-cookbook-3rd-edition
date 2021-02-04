#!/usr/bin/env python
from udp_server import UDPServer
from handler import ThreadPoolHandler, event_loop

pool = None


def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class UDPFibServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(128)
        n = int(msg)
        pool.run(fib, (n,), callback=lambda r: self.respond(r, addr))

    def respond(self, result, addr):
        self.sock.sendto(str(result).encode("ascii"), addr)


if __name__ == "__main__":
    pool = ThreadPoolHandler(num_workers=16)
    handlers = [pool, UDPFibServer(("", 16000))]
    event_loop(handlers)
