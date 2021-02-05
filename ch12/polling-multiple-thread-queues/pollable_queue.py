#!/usr/bin/env python
import socket
from queue import Queue
from select import select


class PollableQueue(Queue):
    def __init__(self):
        super().__init__()
        self._putsocket, self._getsocket = socket.socketpair()

    def fileno(self):
        return self._getsocket.fileno()

    def put(self, item):
        super().put(item)
        self._putsocket.send(b"x")

    def get(self):
        self._getsocket.recv(1)
        return super().get()


def consumer(qs):
    while True:
        can_read, _, _ = select(qs, [], [])
        for r in can_read:
            item = r.get()
            print("got:", item)


if __name__ == "__main__":
    from threading import Thread
    from time import sleep

    q1 = PollableQueue()
    q2 = PollableQueue()
    q3 = PollableQueue()
    t = Thread(target=consumer, args=([q1, q2, q3],), daemon=True)
    t.start()

    q1.put(1)
    q2.put(10)
    q3.put("hello")
    q2.put(15)

    sleep(1)
