import unittest

from fff.fuzzyfile import FuzzyFile

FAKE_FILE = '/home/jeff/bogusfile.txt'

class TestFuzzyFile(unittest.TestCase):

    def setUp(self):
        self.ff = FuzzyFile(FAKE_FILE)

    def test_initialization(self):
        f = FuzzyFile(FAKE_FILE)
        self.assertEqual(f.ext, 'txt')
        self.assertEqual(f.name, 'bogusfile.txt')
        self.assertEqual(f.dir, '/home/jeff')
        self.assertEqual(f.path, FAKE_FILE)
        self.assertEqual(f.score, 0)
        self.assertEqual(f.head, 0)
        self.assertEqual(f.tail, 0)
        self.assertFalse(f.matched)

    def test_str(self):
        self.assertEqual(str(self.ff), FAKE_FILE)

if __name__ == '__main__':
    unittest.main()
