#!/usr/bin/env python
from queue import Queue
from threading import Thread, Event


class ActorExit(Exception):
    pass


class Actor:
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()

        return msg

    def close(self):
        self.send(ActorExit)

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap, daemon=True)
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        while True:
            self.recv()


class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print("got:", msg)


class TaggedActor(Actor):
    def run(self):
        while True:
            tag, *payload = self.recv()
            getattr(self, f"do_{tag}")(*payload)

    def do_a(self, x):
        print("running a", x)

    def do_b(self, x, y):
        print("running b", x, y)


if __name__ == "__main__":
    p = PrintActor()
    p.start()
    p.send("hello")
    p.send("world")
    p.close()
    p.join()

    a = TaggedActor()
    a.start()
    a.send(("a", 1))
    a.send(("b", 2, 3))
    a.close()
    a.join()
