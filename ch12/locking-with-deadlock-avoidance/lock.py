#!/usr/bin/env python
import threading
import time
from contextlib import contextmanager

_local = threading.local()


@contextmanager
def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))
    acquired = getattr(_local, "acquired", [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError("lock order violation")

    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks) :]


x_lock, y_lock = threading.Lock(), threading.Lock()


def thread_1():
    while True:
        with acquire(x_lock, y_lock):
            print("thread-1")


def thread_2():
    while True:
        with acquire(y_lock, x_lock):
            print("thread-2")


if __name__ == "__main__":
    t1 = threading.Thread(target=thread_1, daemon=True)
    t1.start()

    t2 = threading.Thread(target=thread_2, daemon=True)
    t2.start()

    time.sleep(1)
