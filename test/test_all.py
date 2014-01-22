import unittest
from test_fuzzyfile import TestFuzzyFile


result = unittest.TestResult()
fuzzy_file_suite = unittest.TestLoader().loadTestsFromTestCase(TestFuzzyFile)

all_test_suite = unittest.TestSuite([fuzzy_file_suite])

all_test_suite.run(result)
print result
