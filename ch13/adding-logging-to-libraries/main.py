#!/usr/bin/env python
import logging
import some_lib


logging.basicConfig()
logging.getLogger(some_lib.__name__).level = logging.DEBUG
some_lib.func()
