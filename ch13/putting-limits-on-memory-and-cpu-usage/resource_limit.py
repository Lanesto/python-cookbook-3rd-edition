#!/usr/bin/env python
import signal
import resource
import os


def time_exceeded(sig_no, frame):
    print("time's up")
    raise SystemExit(1)


def set_max_runtime(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    signal.signal(signal.SIGXCPU, time_exceeded)


if __name__ == "__main__":
    set_max_runtime(15)
    while True:
        pass
