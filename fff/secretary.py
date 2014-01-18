#!/usr/bin/python

import os
import sys
sys.path.append(os.path.dirname(__file__))

from fuzzyindex import fuzzyindex

root = sys.argv[1]
pat = sys.argv[2]
focus = sys.argv[3:]

FI = fuzzyindex.FuzzyIndex(root, focus_files=focus)

f = FI.match(pat)
print f.name
print f.path
