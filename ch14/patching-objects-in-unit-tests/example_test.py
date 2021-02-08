#!/usr/bin/env python
import unittest
from unittest.mock import patch
import example


@patch("example.func")
def test_func(x, mock_func):
    example.func(x)
    mock_func.assert_called_with(x)


if __name__ == "__main__":
    test_func(1)
