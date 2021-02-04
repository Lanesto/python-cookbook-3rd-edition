#!/usr/bin/env python
from zerocopy import send_from


if __name__ == "__main__":
    import socket
    import numpy

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 25000))
    s.listen(1)
    client, addr = s.accept()

    arr = numpy.arange(0.0, 5000000.0)
    send_from(arr, client)
