#!/usr/bin/env python

if __name__ == "__main__":
    import importlib

    math = importlib.import_module("math")
    print(math.sqrt(2))

    spam = importlib.import_module("my_package.spam")
