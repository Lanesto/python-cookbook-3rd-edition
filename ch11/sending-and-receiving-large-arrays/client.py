#!/usr/bin/env python
from zerocopy import recv_into


if __name__ == "__main__":
    import socket
    import numpy

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 25000))
    arr = numpy.zeros(shape=5000000, dtype=float)
    recv_into(arr, sock)
    print(arr[0:100])
