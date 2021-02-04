import select
import os
import socket
from concurrent.futures import ThreadPoolExecutor


class EventHandler:
    def fileno(self):
        raise NotImplemented

    def wants_to_receive(self):
        return False

    def handle_receive(self):
        pass

    def wants_to_send(self):
        return False

    def handle_send(self):
        pass


class ThreadPoolHandler(EventHandler):
    def __init__(self, num_workers):
        if os.name == "posix":
            self.signal_done_sock, self.done_sock = socket.socketpair()
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            self.signal_done_sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self.done_sock, _ = server.accept()
            server.close()

        self.pending = []
        self.pool = ThreadPoolExecutor(num_workers)

    def fileno(self):
        return self.done_sock.fileno()

    def _complete(self, callback, r):
        self.pending.append((callback, r.result()))
        self.signal_done_sock.send(b"x")

    def run(self, func, args=(), kwargs={}, *, callback):
        r = self.pool.submit(func, *args, **kwargs)
        r.add_done_callback(lambda r: self._complete(callback, r))

    def wants_to_receive(self):
        return True

    def handle_receive(self):
        for callback, result in self.pending:
            callback(result)
            self.done_sock.recv(1)
        self.pending = []


def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        for h in can_recv:
            h.handle_receive()

        for h in can_send:
            h.handle_send()
