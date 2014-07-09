#!/usr/bin/env python
import os
os.system('find . -type f \( -name  \*.pyc -o -name \*.orig \) -exec rm {} \;');
