import os
import shutil
import unittest

from fff.fuzzyindex import FuzzyIndex
from fff import MATCH_LEVELS, IGNORE_DIRS, IGNORE_FILES

ROOT = 'tmp'

FOCUS_FILES = ['dir0_file1.ext']

IGNORE = [
'tmp/dir2/py.pyc',
'tmp/dir2/__init__.py',
'tmp/.git/nomatch.ext'
]

FILES = [
'tmp/dir0_file1.ext',
'tmp/dir1/dir1_file1.ext',
'tmp/dir1/dir1_file2.ext',
'tmp/dir2/dir2_file1.ext',
'tmp/dir2/dir2_file2.ext',
]

FILE_SYSTEM = FILES + IGNORE

class TestFuzzyIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ setup the test directory. """
        def makefile(path):
            basedir = os.path.dirname(path)
            if not os.path.exists(basedir):
                os.makedirs(basedir)
            open(path, 'a').close()

        for f in FILE_SYSTEM:
            makefile(f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(ROOT)

    def setUp(self):
        self.fi = FuzzyIndex(ROOT, ignore_dirs=IGNORE_DIRS, ignore_files=IGNORE_FILES)

    def test_init(self):
        self.assertEqual(len(self.fi.files), 5)

    def test_append(self):
        FILE = '/path/to/file.ext'
        self.fi.append(FILE)
        self.assertEqual(self.fi.files[-1].path, FILE)

    def test_generate_paths(self):
        paths = [x for x in self.fi.generate_paths(ROOT, ignore_dirs=IGNORE_DIRS, ignore_files=IGNORE_FILES)]
        paths.sort()
        FILES.sort()
        self.assertEqual(paths, FILES)

    def test_generate_paths_focus(self):
        paths = [os.path.basename(x) for x in self.fi.generate_paths(ROOT, focus_files=FOCUS_FILES)]
        paths.sort()
        FOCUS_FILES.sort()
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths, FOCUS_FILES)

    def test_generate_patterns(self):
        patts = [x.pattern for x in self.fi.generate_patterns('ab')]
        self.assertEqual(len(patts), MATCH_LEVELS)
        patterns = ['^(?P<head>.*?)a(.{{,{0}}}?)b(?P<tail>.*?)$'.format(i) for i in range(MATCH_LEVELS)]
        self.assertEqual(patts, patterns)        

    def test_match(self):
        NO_MATCH = ' '
        self.assertEqual(self.fi.match(NO_MATCH), None)
