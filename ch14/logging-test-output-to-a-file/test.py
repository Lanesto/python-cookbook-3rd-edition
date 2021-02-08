#!/usr/bin/env python
import unittest
import sys
from io import StringIO


class MyTest(unittest.TestCase):
    def test_not_ok(self):
        self.assertTrue(False)


def main(out=sys.stderr, verbosity=2):
    loader = unittest.TestLoader()
    test_suites = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity=verbosity).run(test_suites)


if __name__ == "__main__":
    with StringIO() as f:
        main(f)
        result = f.getvalue()

    print(result)
