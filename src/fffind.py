#!/usr/bin/python

import os
import sys
import argparse

from fuzzyindex import fuzzyindex

IGNORE_DIRS = ['.git', '.svn', 'build']
IGNORE_FILES = [r'\.pyc$', r'^\.bash', r'^\.git', r'^__']


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", help="Top-level directory from which to scan.", default=os.getcwd())
parser.add_argument("pattern", help="Pattern to match based on. Does not understand regex so don't try :).")
parser.add_argument("-f", "--focus", help="Limit the search to these files.", nargs="*", default=[])
parser.add_argument("-if", "--ignore-files", help="Ignore files that match the given patterns", nargs="*", default=IGNORE_FILES)
parser.add_argument("-id", "--ignore-dirs", help="Do not scan into the given directory names", nargs="*", default=IGNORE_DIRS)
parser.add_argument("-l", "--list", help="List all of the matched files instead of picking the 'best' one.", action="store_true")
args = parser.parse_args()

FI = fuzzyindex.FuzzyIndex(args.root, ignore_dirs=args.ignore_dirs, ignore_files=args.ignore_files, focus_files=[])

f = FI.match(args.pattern, list_files=args.list)

if args.list:
    for m in f:
        print m
else:
    print f
