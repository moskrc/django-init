#!/usr/bin/env python
import os
os.system("find . -name \"*.pyc\" -exec rm {} \;")
os.system("find . -name \"*.orig\" -exec rm {} \;")
