#!/usr/bin/env python
import time
from threading import Thread, Event


def countdown(n, started_evt):
    time.sleep(3)
    print("countdown starting")
    started_evt.set()
    while n > 0:
        print("T-minus", n)
        n -= 1
        time.sleep(1)


if __name__ == "__main__":
    started_evt = Event()

    print("launching countdown")
    t = Thread(target=countdown, args=(5, started_evt))
    t.start()

    started_evt.wait()
    print("countdown is running")
    t.join()
