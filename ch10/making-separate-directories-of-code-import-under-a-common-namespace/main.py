#!/usr/bin/env python
import sys

sys.path.extend(("foo-package", "bar-package"))

import spam.blah
import spam.grok

if __name__ == "__main__":
    print(dir(spam))
