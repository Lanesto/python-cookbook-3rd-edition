#!/usr/bin/env python

"""
Without importer

    >>> import fib
    Traceback (most recent call last):
        ...
    ModuleNotFoundError: No module named 'fib'

Install import hook

    >>> import urlimport_hook
    >>> urlimport_hook.install_path_hook()
    >>> import fib
    Traceback (most recent call last):
        ...
    ModuleNotFoundError: No module named 'fib'

Add entry to path

    >>> import sys
    >>> sys.path.append('http://localhost:15000')
    >>> import fib
    i'm fib
    >>> import grok.blah
    i'm grok.__init__
    i'm grok.blah
    >>> grok.blah.__file__
    'http://localhost:15000/grok/blah.py'


"""

if __name__ == "__main__":
    import doctest

    doctest.testmod()
