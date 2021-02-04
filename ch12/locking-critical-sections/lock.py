#!/usr/bin/env python
import threading
import time


class SharedCounter:
    _value_lock = threading.Lock()

    def __init__(self, initial_value=0):
        self._value = initial_value

    def incr(self, delta=1):
        cls = self.__class__
        with cls._value_lock:
            self._value += delta

    def decr(self, delta=1):
        cls = self.__class__
        with cls._value_lock:
            self._value -= delta


def fire(counter):
    for _ in range(100):
        counter.incr()
        time.sleep(0.01)

    print(counter._value)


if __name__ == "__main__":
    counter = SharedCounter()

    for _ in range(10):
        t = threading.Thread(target=fire, args=(counter,))
        t.start()

    print(counter._value)
    time.sleep(10)
