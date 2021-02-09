#!/usr/bin/env python
import warnings


def func(x, y, logfile=None, debug=False):
    if logfile is not None:
        warnings.warn("logfile argument deprecated", DeprecationWarning)


if __name__ == "__main__":
    func(1, 2, logfile=object())
