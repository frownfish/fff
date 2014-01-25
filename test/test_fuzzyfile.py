import re
import unittest

from fff.fuzzyfile import FuzzyFile
from fff import MATCH_LEVELS, CAPTURE, HEAD, TAIL


FAKE_FILE = '/home/jeff/bogusfile.txt'


class TestFuzzyFile(unittest.TestCase):

    def setUp(self):
        self.f = FuzzyFile(FAKE_FILE)

    def gen_patterns(self, pattern):
        patterns = []
        for level in range(MATCH_LEVELS):
            segments = [re.escape(x) for x in list(pattern)]
            patterns.append(re.compile(HEAD + CAPTURE.format(level).join(segments) + TAIL))
        return patterns

    def test_initialization(self):
        f = FuzzyFile(FAKE_FILE)
        self.assertEqual(self.f.ext, 'txt')
        self.assertEqual(self.f.name, 'bogusfile.txt')
        self.assertEqual(self.f.dir, '/home/jeff')
        self.assertEqual(self.f.path, FAKE_FILE)
        self.assertEqual(self.f.score, 0)
        self.assertEqual(self.f.head, 0)
        self.assertEqual(self.f.tail, 0)
        self.assertFalse(self.f.matched)

    def test_str(self):
        self.assertEqual(str(self.f), FAKE_FILE)

    def test_bool(self):
        self.assertFalse(self.f)
        self.f.matched = True
        self.assertTrue(self.f)

    def test_lt(self):
        other = FuzzyFile('home/jeff/otherfile.txt')
        self.assertFalse(self.f < other)
        self.assertFalse(other < self.f)
        self.f.matched = True
        self.assertLess(self.f, other)
        other.matched = True
        self.f.score = 0
        other.score = 2
        self.assertLess(self.f, other)
        other.score = 0
        self.f.head = 0
        other.head = 2
        self.assertLess(self.f, other)
        other.head = 0
        self.f.tail = 0
        other.tail = 2
        self.assertLess(self.f, other)
        other.tail = 0
        self.assertLess(self.f, other)
        self.assertRaises(NotImplementedError, self.f.__lt__, 0)

    def test_match_filename_level_0(self):
        pattern = 'bog'
        patterns = self.gen_patterns(pattern)

        self.assertFalse(self.f.matched)
        self.f.match(patterns)
        self.assertTrue(self.f.matched)
        self.assertEqual(self.f.score, 0)
        self.assertEqual(self.f.head, 0)
        self.assertEqual(self.f.tail, 10)

    def test_match_filename_level_1(self):
        pattern = 'bgs'
        patterns = self.gen_patterns(pattern)

        self.assertFalse(self.f.matched)
        self.f.match(patterns)
        self.assertTrue(self.f.matched)
        self.assertEqual(self.f.score, 2)
        self.assertEqual(self.f.head, 0)
        self.assertEqual(self.f.tail, 8)

    def test_match_filename_level_2(self):
        pattern = 'oi'
        patterns = self.gen_patterns(pattern)

        self.assertFalse(self.f.matched)
        self.f.match(patterns)
        self.assertTrue(self.f.matched)
        self.assertEqual(self.f.score, 4)
        self.assertEqual(self.f.head, 1)
        self.assertEqual(self.f.tail, 6)

    def test_match_path(self):
        pattern = 'jef/bog.txt'
        patterns = self.gen_patterns(pattern)

        self.assertFalse(self.f.matched)
        self.f.match(patterns, include_path=True)
        self.assertTrue(self.f.matched)
        self.assertEqual(self.f.score, 7)
        self.assertEqual(self.f.head, 6)
        self.assertEqual(self.f.tail, 0)


if __name__ == '__main__':
    unittest.main()
