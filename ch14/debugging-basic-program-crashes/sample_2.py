#!/usr/bin/env python
# import sys
# import traceback
import pdb


def sample(n):
    if n > 0:
        sample(n - 1)
    else:
        # traceback.print_stack(file=sys.stdout)
        pdb.set_trace()


sample(5)
