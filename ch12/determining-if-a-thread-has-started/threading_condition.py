#!/usr/bin/env python
import threading
import time


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self):
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


def countdown(n_ticks):
    while n_ticks > 0:
        ptimer.wait_for_tick()
        print("T-minus", n_ticks)
        n_ticks -= 1


def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print("counting", n)
        n += 1


if __name__ == "__main__":
    ptimer = PeriodicTimer(2)
    ptimer.start()
    threading.Thread(target=countdown, args=(10,)).start()
    threading.Thread(target=countup, args=(5,)).start()
