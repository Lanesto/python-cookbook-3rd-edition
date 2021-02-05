#!/usr/bin/env python
import os
import sys
import atexit
import signal


def daemonize(
    pidfile, *, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"
):
    if os.path.exists(pidfile):
        raise RuntimeError("already running")

    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError("fork #1 failed")

    os.chdir("/")
    os.umask(0)
    os.setsid()
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError("fork #2 failed")

    sys.stdout.flush()
    sys.stderr.flush()
    with open(stdin, "rb", 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, "ab", 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, "ab", 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    with open(pidfile, "w") as f:
        print(os.getpid(), file=f)

    atexit.register(lambda: os.remove(pidfile))

    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


def main():
    import time

    sys.stdout.write("daemon started with pid {}\n".format(os.getpid()))
    while True:
        sys.stdout.write("daemon alive! {}\n".format(time.ctime()))
        time.sleep(3)


if __name__ == "__main__":
    pidfile = "/tmp/daemon.pid"

    if len(sys.argv) != 2:
        print("usage: {} [start|stop]".format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if sys.argv[1] == "start":
        try:
            daemonize(
                pidfile, stdout="/tmp/daemon.log", stderr="/tmp/daemon.log"
            )
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)

        main()
    elif sys.argv[1] == "stop":
        if os.path.exists(pidfile):
            with open(pidfile) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print("not running", file=sys.stderr)
            raise SystemExit(1)
    else:
        print("unknown command {!r}".format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
