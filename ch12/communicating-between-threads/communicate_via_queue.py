#!/usr/bin/env python
import random
import time
from threading import Thread
from queue import Queue

_sentinel_exit = object()


def producer(out_q):
    n = 0
    while n < 10:
        data = random.randint(1, 100)
        out_q.put(data)
        n += 1
        time.sleep(1)

    out_q.put(_sentinel_exit)


def consumer(in_q):
    while True:
        data = in_q.get()
        if data is _sentinel_exit:
            in_q.put(data)
            break

        print(data)


if __name__ == "__main__":
    q = Queue()
    Thread(target=producer, args=(q,)).start()
    Thread(target=consumer, args=(q,)).start()
