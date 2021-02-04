#!/usr/bin/env python
import threading
import time


def countdown(n):
    while n > 0:
        print("T-minus", n)
        n -= 1
        time.sleep(1)


if __name__ == "__main__":
    print("run")
    t = threading.Thread(target=countdown, args=(10,), daemon=True)
    t.start()
    print("quit")
