#!/usr/bin/env python
from math import sqrt


def compute_roots(nums):
    result = []
    result_append = result.append
    for n in nums:
        result_append(sqrt(n))

    return result


nums = range(1000000)
compute_roots(nums)
