#!/usr/bin/env python
import os


width = os.get_terminal_size().columns
print(format("hello world", f"^{width}s"))
