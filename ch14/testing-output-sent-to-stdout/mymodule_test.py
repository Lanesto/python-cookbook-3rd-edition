#!/usr/bin/env python
import unittest
from io import StringIO
from unittest.mock import patch
import mymodule


class TestURLPrint(unittest.TestCase):
    def test_url_gets_to_stdout(self):
        protocol = "http"
        host = "www"
        domain = "example.com"
        expected_url = "http://www.example.com"
        with patch(target="sys.stdout", new=StringIO()) as fake_out:
            mymodule.urlprint(protocol, host, domain)
            self.assertEqual(fake_out.getvalue().strip(), expected_url)


if __name__ == "__main__":
    unittest.main()
