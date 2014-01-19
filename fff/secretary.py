#!/usr/bin/python

import os
import sys
import argparse

sys.path.append(os.path.dirname(__file__))

from fuzzyindex import fuzzyindex

IGNORE_DIRS = ['.git', '.svn']
IGNORE_FILES = [r'\.pyc$', r'^\.bash', r'^\.git']


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", help="Top-level directory from which to scan.", default=os.getcwd())
parser.add_argument("pattern", help="Pattern to match based on. Does not understand regex so don't try :).")
parser.add_argument("-f", "--focus", help="Limit the search to these files.", nargs="*", default=[])
parser.add_argument("-if", "--ignore-files", help="Ignore files that match the given patterns", nargs="*", default=IGNORE_FILES)
parser.add_argument("-id", "--ignore-dirs", help="Do not scan into the given directory names", nargs="*", default=IGNORE_DIRS )
args = parser.parse_args()

FI = fuzzyindex.FuzzyIndex(args.root, ignore_dirs=args.ignore_dirs, ignore_files=args.ignore_files, focus_files=[])

f = FI.match(args.pattern)
print f.path
