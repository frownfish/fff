import os
import unittest

from fff.fuzzyindex import FuzzyIndex
from fff.fuzzyfile import FuzzyFile
from fff import MATCH_LEVELS, IGNORE_DIRS, IGNORE_FILES

from test import setup_file_system, cleanup_file_system
from test import FILE_SYSTEM, FOCUS_FILES, TEST_ROOT, FAKE_FILE, PATH_SEP, NO_MATCH


class TestFuzzyIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ setup the test directory. """
        setup_file_system(FILE_SYSTEM)

    @classmethod
    def tearDownClass(cls):
        cleanup_file_system(TEST_ROOT)
        

    def setUp(self):
        self.fi = FuzzyIndex(TEST_ROOT, ignore_dirs=IGNORE_DIRS, ignore_files=IGNORE_FILES)

    def test_init(self):
        self.assertEqual(len(self.fi.files), 5)

    def test_append(self):
        self.fi.append(FAKE_FILE)
        self.assertEqual(self.fi.files[-1].path, FAKE_FILE)

    def test_generate_paths(self):
        paths = list(self.fi.generate_paths(TEST_ROOT))
        paths.sort()
        FILE_SYSTEM.sort()
        self.assertEqual(paths, FILE_SYSTEM)

    def test_generate_paths_filter_dirs(self):
        p = list(self.fi.generate_paths(TEST_ROOT, ignore_dirs=['dir1', 'dir2']))
        self.assertEqual(p, ['tmp/dir0_file1.ext', 'tmp/.git/nomatch.ext'])

    def test_generate_paths_filter_files(self):
        p = list(self.fi.generate_paths(TEST_ROOT, ignore_files=[r'\.pyc$', r'\.py$', r'\.ext$']))
        self.assertEqual(p, [])

    def test_generate_paths_focus(self):
        paths = list(self.fi.generate_paths(TEST_ROOT, focus_files=[FOCUS_FILES[0].lstrip(TEST_ROOT).lstrip(PATH_SEP)]))
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
        m = self.fi.match(NO_MATCH)
        self.assertEqual(m, None)

    def test_match(self):
        m = self.fi.match('d1_f1')
        self.assertEqual(m.path, 'tmp/dir1/dir1_file1.ext')

    def test_match_include_dir(self):
        m = self.fi.match('/file1')
        self.assertEqual(m.path, 'tmp/dir0_file1.ext')

    def test_match_list(self):
        m = self.fi.match('dir1_', list_files=True)
        self.assertEqual(type(m), list)
        self.assertEqual(len(m), 2)
        L1 = [x.path for x in m]
        L1.sort()
        L2 = ['tmp/dir1/dir1_file1.ext',
              'tmp/dir1/dir1_file2.ext']
        self.assertEqual(L1, L2)

    def test_match_none_list(self):
        m = self.fi.match(NO_MATCH, list_files=True)
        self.assertEqual(m, [])
