#!/usr/bin/env python
import threading
import time


def worker(n, semaphore):
    if not semaphore.acquire(timeout=3):
        print("exit", n)
        return

    print("working", n)


if __name__ == "__main__":
    semaphore = threading.Semaphore(3)
    n_workers = 10
    for n in range(n_workers):
        t = threading.Thread(target=worker, args=(n, semaphore))
        t.start()

    for _ in range(7):
        semaphore.release()
        time.sleep(0.5)

    t.join()
