#!/usr/bin/env python
import time
from functools import wraps
from contextlib import contextmanager


def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"[{elapsed:.8f}] {func.__module__}.{func.__qualname__}")
        return result

    return wrapper


@contextmanager
def time_block(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        elapsed = end - start
        print(f"[{elapsed:.8f}] {label}")


@time_this
def countdown(n):
    while n > 0:
        n -= 1


if __name__ == "__main__":
    countdown(2e7)

    with time_block("sleep"):
        time.sleep(5)
