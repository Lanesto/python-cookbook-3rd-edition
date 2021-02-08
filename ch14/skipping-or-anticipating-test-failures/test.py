#!/usr/bin/env python
import unittest
import os
import platform


class SomeTest(unittest.TestCase):
    def test_0(self):
        self.assertTrue(True)

    @unittest.skip("skip")
    def test_1(self):
        self.fail("should have failed")

    @unittest.skipIf(os.name == "posix", "not supported on unix")
    def test_2(self):
        import winreg

    @unittest.skipUnless(platform.system() == "Darwin", "mac specific test")
    def test_3(self):
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_4(self):
        self.assertEqual(2 + 2, 5)


if __name__ == "__main__":
    unittest.main()
