#!/usr/bin/python

import os
import sys
import argparse

from fff import EXCLUDE_DIRS, EXCLUDE_FILES, ROOT
from fff.fuzzyindex import FuzzyIndex


def main(args=None):
    args = _build_parser().parse_args(args=args)
    FI = FuzzyIndex(args.root, exclude_dirs=args.exclude_dirs, exclude_files=args.exclude_files, focus_files=args.focus_files)
    f = FI.match(args.pattern, list_files=args.list)
    return _output(f, args)


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Pattern to match based on. Does not understand regex so don't try :).")
    parser.add_argument("-r", "--root", help="Top-level directory from which to scan.", default=os.getcwd())
    parser.add_argument("-ff", "--focus-files", help="Limit the search to these files.", nargs="*", default=[])
    parser.add_argument("-ef", "--exclude-files", help="Ignore files that match the given patterns", nargs="*", default=EXCLUDE_FILES)
    parser.add_argument("-ed", "--exclude-dirs", help="Do not scan into the given directory names", nargs="*", default=EXCLUDE_DIRS)
    parser.add_argument("-l", "--list", help="List all of the matched files instead of picking the 'best' one.", action="store_true")
    parser.add_argument("-p", help="print the matched file(s) on the command line. Default is to return the path or list of paths to the files.", action="store_true")
    return parser


def _output(f, args):
    if args.list:
        r = [x.path for x in f]
        if args.p:
            print r
        else:
            return r
    else:
        if args.p:
            print f.path if f is not None else None
        else:
            return f.path if f is not None else None

if __name__ == '__main__':  # pragma: no cover
    main()
