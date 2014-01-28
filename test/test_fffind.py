import argparse
import unittest

from fff import fffind, EXCLUDE_DIRS, EXCLUDE_FILES, ROOT
from fff.fuzzyfile import FuzzyFile

from test import FAKE_FILE


class TestFffind(unittest.TestCase):

    def setUp(self):
        pass

    def test_output(self):
        f = FuzzyFile(FAKE_FILE)

        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--list", help="List all of the matched files instead of picking the 'best' one.", action="store_true")
        parser.add_argument("-p", help="print the matched file(s) on the command line. Default is to return the path or list of paths to the files.", action="store_true")

        args = ['--list', '-p']
        args = parser.parse_args(args)

        r = fffind._output([f], args)
        self.assertEqual(type(r), type(None))
        
        args = ['-p']
        args = parser.parse_args(args)
        r = fffind._output(f, args)
        self.assertEqual(type(r), type(None))

        args = ['--list']
        args = parser.parse_args(args)
        r = fffind._output([f], args)
        self.assertEqual(type(r), list)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], FAKE_FILE)

        args = []
        args = parser.parse_args(args)
        r = fffind._output(f, args)
        self.assertEqual(type(r), str)
        self.assertEqual(r, FAKE_FILE)

    def test_build_parser(self):
        p = fffind._build_parser()
        args = p.parse_args(['this'])
        self.assertEqual(args.pattern, 'this')
        self.assertEqual(args.root, ROOT)
        self.assertEqual(args.focus_files, [])
        self.assertEqual(args.exclude_files, EXCLUDE_FILES)
        self.assertEqual(args.exclude_dirs, EXCLUDE_DIRS)
        self.assertFalse(args.list)
        self.assertFalse(args.p)


    def test_main(self):
        args = [' ']
        self.assertEqual(fffind.main(args), None)
        args.append('--list')
        self.assertEqual(fffind.main(args), [])
