#!/usr/bin/env python
import socket
from multiprocessing.connection import Listener
from multiprocessing.reduction import send_handle


def server(work_addr, port):
    work_server = Listener(work_addr, authkey=b"peekaboo")
    worker = work_server.accept()
    worker_pid = worker.recv()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(("", port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print("server: got connection from", addr)
        send_handle(worker, client.fileno(), worker_pid)
        client.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("usage: {} server addr port".format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))