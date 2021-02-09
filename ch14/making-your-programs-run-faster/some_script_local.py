#!/usr/bin/env python
import math


def compute_roots(nums):
    result = []
    for n in nums:
        result.append(math.sqrt(n))

    return result


nums = range(10000000)
compute_roots(nums)
