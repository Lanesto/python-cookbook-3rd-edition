#!/usr/bin/env python
import threading
import queue
import random

running = True

_sentinel = object()


def producer(out_q):
    n = 0
    while running:
        n += 1
        evt = threading.Event()
        if n > 10:
            out_q.put((_sentinel, evt))
        else:
            data = random.randint(1, 100)
            out_q.put((data, evt))

        evt.wait()


def consumer(in_q):
    global running
    while True:
        data, evt = in_q.get()
        if data is _sentinel:
            evt.set()
            running = False
            break
        else:
            evt.set()
            print(data)


if __name__ == "__main__":
    q = queue.Queue()
    threading.Thread(target=producer, args=(q,)).start()
    threading.Thread(target=consumer, args=(q,)).start()
