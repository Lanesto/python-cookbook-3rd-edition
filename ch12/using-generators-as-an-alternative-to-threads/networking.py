#!/usr/bin/env python
from collections import deque
from select import select


class YieldEvent:
    def handle_yield(self, sched, task):
        pass

    def handle_resume(self, sched, task):
        pass


class Scheduler:
    def __init__(self):
        self._num_tasks = 0
        self._ready = deque()
        self._read_waiting = {}
        self._write_waiting = {}

    def _iopoll(self):
        rset, wset, xset = select(self._read_waiting, self._write_waiting, [])
        for r in rset:
            evt, task = self._read_waiting.pop(r)
            evt.handle_resume(self, task)

        for w in wset:
            evt, task = self._write_waiting.pop(w)
            evt.handle_resume(self, task)

    def new(self, task):
        self._ready.append((task, None))
        self._num_tasks += 1

    def add_ready(self, task, msg=None):
        self._ready.append((task, msg))

    def _read_wait(self, fileno, evt, task):
        self._read_waiting[fileno] = (evt, task)

    def _write_wait(self, fileno, evt, task):
        self._write_waiting[fileno] = (evt, task)

    def run(self):
        while self._num_tasks:
            if not self._ready:
                self._iopoll()

            task, msg = self._ready.popleft()
            try:
                r = task.send(msg)
                if isinstance(r, YieldEvent):
                    r.handle_yield(self, task)
                else:
                    raise RuntimeError("unrecognized yield event")
            except StopIteration:
                self._num_tasks -= 1


class ReadSocket(YieldEvent):
    def __init__(self, sock, num_bytes):
        self.sock = sock
        self.num_bytes = num_bytes

    def handle_yield(self, sched, task):
        sched._read_wait(self.sock.fileno(), self, task)

    def handle_resume(self, sched, task):
        data = self.sock.recv(self.num_bytes)
        sched.add_ready(task, data)


class WriteSocket(YieldEvent):
    def __init__(self, sock, data):
        self.sock = sock
        self.data = data

    def handle_yield(self, sched, task):
        sched._write_wait(self.sock.fileno(), self, task)

    def handle_resume(self, sched, task):
        num_sent = self.sock.send(self.data)
        sched.add_ready(task, num_sent)


class AcceptSocket(YieldEvent):
    def __init__(self, sock):
        self.sock = sock

    def handle_yield(self, sched, task):
        sched._read_wait(self.sock.fileno(), self, task)

    def handle_resume(self, sched, task):
        r = self.sock.accept()
        sched.add_ready(task, r)


class Socket(object):
    def __init__(self, sock):
        self._sock = sock

    def recv(self, max_bytes):
        return ReadSocket(self._sock, max_bytes)

    def send(self, data):
        return WriteSocket(self._sock, data)

    def accept(self):
        return AcceptSocket(self._sock)

    def __getattr__(self, name):
        return getattr(self._sock, name)


if __name__ == "__main__":
    from socket import socket, AF_INET, SOCK_STREAM
    import time

    def readline(sock):
        chars = []
        while True:
            c = yield sock.recv(1)
            if not c:
                break

            chars.append(c)
            if c == b"\n":
                break

        return b"".join(chars)

    class EchoServer:
        def __init__(self, addr, sched):
            self.sched = sched
            sched.new(self.server_loop(addr))

        def server_loop(self, addr):
            s = Socket(socket(AF_INET, SOCK_STREAM))
            s.bind(addr)
            s.listen(5)
            while True:
                c, a = yield s.accept()
                print("got connection from", a)
                self.sched.new(self.client_handler(Socket(c)))

        def client_handler(self, client):
            while True:
                line = yield from readline(client)
                if not line:
                    break

                line = b"got: " + line
                while line:
                    num_sent = yield client.send(line)
                    line = line[num_sent:]

            client.close()
            print("client closed")

    sched = Scheduler()
    EchoServer(("", 16001), sched)
    sched.run()
