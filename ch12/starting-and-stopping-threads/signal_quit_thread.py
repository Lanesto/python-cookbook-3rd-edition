#!/usr/bin/env python
import time
from threading import Thread


class Countdown:
    def __init__(self):
        self._running = True

    def run(self, n):
        while self._running and n > 0:
            print("T-minus", n)
            n -= 1
            time.sleep(1)

    def terminate(self):
        self._running = False


if __name__ == "__main__":
    c = Countdown()
    t = Thread(target=c.run, args=(5,))
    t.start()
    c.terminate()
    t.join()
