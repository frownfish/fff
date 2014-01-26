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
        paths = list(self.fi.generate_paths(ROOT))
        paths.sort()
        FILE_SYSTEM.sort()
        self.assertEqual(paths, FILE_SYSTEM)

    def test_generate_paths_filter_dirs(self):
        p = list(self.fi.generate_paths(ROOT, ignore_dirs=['dir1', 'dir2']))
        self.assertEqual(p, ['tmp/dir0_file1.ext', 'tmp/.git/nomatch.ext'])

    def test_generate_paths_filter_files(self):
        p = list(self.fi.generate_paths(ROOT, ignore_files=[r'\.pyc$', r'\.py$', r'\.ext$']))
        self.assertEqual(p, [])

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

    def test_match_none(self):
        NO_MATCH = ' '
        self.assertEqual(self.fi.match(NO_MATCH), None)

    def test_match(self):
        m = self.fi.match('d1_f1')
        self.assertEqual(m.path, 'tmp/dir1/dir1_file1.ext')

    def test_match_include_dir(self):
        m = self.fi.match('/file1')
        self.assertEqual(m.path, 'tmp/dir0_file1.ext')

    def test_match_list(self):
        m = self.fi.match('dir1_', list_files=True)
        self.assertTrue(type(m) == list)
        self.assertEqual(len(m), 2)
        L1 = [x.path for x in m]
        L1.sort()
        L2 = ['tmp/dir1/dir1_file1.ext',
              'tmp/dir1/dir1_file2.ext']
        self.assertEqual(L1, L2)
