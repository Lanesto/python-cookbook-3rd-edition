#!/usr/bin/env python
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
import gzip
import glob


def find_robots(gz_filename):
    robots = set()
    with gzip.open(gz_filename, mode="rt", encoding="ascii") as f:
        for line in f:
            fields = line.split()
            client_ip, url = fields[0], fields[6]
            if url == "/robots.txt":
                robots.add(client_ip)

    return robots


def find_all_robots(log_dir):
    filenames = glob.glob(f"{log_dir}/*.log.gz")
    all_robots = set()
    with ProcessPoolExecutor() as pool:
        for robots in pool.map(find_robots, filenames):
            all_robots.update(robots)

    return all_robots


if __name__ == "__main__":
    robots = list(find_all_robots("logs"))
    num_robots = len(robots)
    n = 8
    aligner = partial(
        lambda value, format_spec: format(value, format_spec),
        format_spec=">15s",
    )
    for i in range(0, len(robots), n):
        print(
            *map(
                aligner,
                robots[i : min(num_robots, i + n)],
            )
        )
