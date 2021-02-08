#!/usr/bin/env python
import argparse


parser = argparse.ArgumentParser(description="search some files")
parser.add_argument(
    "-p",
    "--pattern",
    metavar="pattern",
    required=True,
    dest="patterns",
    action="append",
    help="text pattern to search for",
)
parser.add_argument(dest="filenames", metavar="filename", nargs="+")
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="verbose mode"
)
parser.add_argument(
    "-o",
    "--out-file",
    dest="out_file",
    action="store",
    help="output file",
    nargs=2,
)
parser.add_argument(
    "-s",
    "--speed",
    action="store",
    choices={"slow", "fast"},
    default="slow",
    help="search speed",
)

args = parser.parse_args()

print(dir(args))
print(args.filenames)
print(args.patterns)
print(args.verbose)
print(args.out_file)
print(args.speed)
