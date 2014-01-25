#!/usr/bin/python

import os
import sys
import argparse

from fff import IGNORE_DIRS, IGNORE_FILES, ROOT

from fff.fuzzyindex import FuzzyIndex


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", help="Top-level directory from which to scan.", default=os.getcwd())
    parser.add_argument("pattern", help="Pattern to match based on. Does not understand regex so don't try :).")
    parser.add_argument("-f", "--focus", help="Limit the search to these files.", nargs="*", default=[])
    parser.add_argument("-if", "--ignore-files", help="Ignore files that match the given patterns", nargs="*", default=IGNORE_FILES)
    parser.add_argument("-id", "--ignore-dirs", help="Do not scan into the given directory names", nargs="*", default=IGNORE_DIRS)
    parser.add_argument("-l", "--list", help="List all of the matched files instead of picking the 'best' one.", action="store_true")
    parser.add_argument("-p", help="print the matched file(s) on the command line. Default is to return the path or list of paths to the files.", action="store_true")
    args = parser.parse_args(args=args)

    FI = FuzzyIndex(args.root, ignore_dirs=args.ignore_dirs, ignore_files=args.ignore_files, focus_files=[])

    f = FI.match(args.pattern, list_files=args.list)
    return _output(f, args)


def _output(f, args):
    if args.list:
        r = [x.path for x in f]
        if args.p:
            print r
        else:
            return r
    else:
        if args.p:
            print f.path
        else:
            return f.path

if __name__ == '__main__':
    main()
