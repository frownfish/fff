import os
import unittest

from fff.fuzzyindex import FuzzyIndex
from fff.fuzzyfile import FuzzyFile
from fff import MATCH_LEVELS, EXCLUDE_DIRS, EXCLUDE_FILES

from test import setup_file_system, cleanup_file_system
from test import FILE_SYSTEM, FOCUS_FILES, TEST_ROOT, FAKE_FILE, PATH_SEP, NO_MATCH, IGNORE


class TestFuzzyIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ setup the test directory. """
        setup_file_system(FILE_SYSTEM)

    @classmethod
    def tearDownClass(cls):
        cleanup_file_system(TEST_ROOT)
        
    def setUp(self):
        self.fi = FuzzyIndex(TEST_ROOT, exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)

    def test_init(self):
        self.assertEqual(len(self.fi.files), len(FILE_SYSTEM) - len(IGNORE))

    def test_append(self):
        self.fi.append(FAKE_FILE)
        self.assertEqual(self.fi.files[-1].path, FAKE_FILE)

    def test_extend(self):
        other = FuzzyIndex(TEST_ROOT)
        other.files = []
        other.append(FAKE_FILE)
        self.assertFalse(FAKE_FILE in [x.path for x in self.fi.files])
        self.fi.extend(other)
        self.assertTrue(FAKE_FILE in [x.path for x in self.fi.files])
        self.assertRaises(NotImplementedError, self.fi.extend, 0)

    def test_exclude_dirs(self):
        p = list(self.fi.filter_dirs(['dir1', 'dir2', 'tmp', '.git'], exclude_dirs=['dir1', 'dir2']))
        p.sort()
        self.assertEqual(p, ['.git', 'tmp'])

    def test_filter_files_exclude_files(self):
        p = list(self.fi.filter_files(IGNORE, exclude_files=[r'\.pyc$', r'\.py$', r'\.ext$']))
        self.assertEqual(p, [])

    def test_filter_files_focus_files(self):
        paths = list(self.fi.filter_files(FILE_SYSTEM, focus_files=FOCUS_FILES))
        paths.sort()
        FOCUS_FILES.sort()
        self.assertEqual(len(paths), len(FOCUS_FILES))
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
