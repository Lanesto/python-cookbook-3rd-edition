#!/usr/bin/env python
import fileinput


with fileinput.input() as f:
    for line in f:
        print(f.filename(), f.fileno(), line, end="")
