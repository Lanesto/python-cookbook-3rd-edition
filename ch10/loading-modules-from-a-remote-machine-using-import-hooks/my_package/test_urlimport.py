#!/usr/bin/env python

"""
Without importer

    >>> import fib
    Traceback (most recent call last):
        ...
    ModuleNotFoundError: No module named 'fib'

Load importer

    >>> import urlimport
    >>> urlimport.install_meta('http://localhost:15000')
    >>> import fib
    i'm fib
    >>> import spam
    i'm spam
    >>> import grok.blah
    i'm grok.__init__
    i'm grok.blah
    >>> grok.blah.__file__
    'http://localhost:15000/grok/blah.py'

"""

if __name__ == "__main__":
    import doctest

    doctest.testmod()
