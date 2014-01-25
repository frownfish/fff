import os
import sys
import re
import logging

import fuzzyfile

MATCH_LEVELS = 20
CAPTURE = "(.{{,{0}}}?)"
HEAD = "^(?P<head>.*?)"
TAIL = "(?P<tail>.*?)$"


class FuzzyIndex:
    """ class to hold isntances of the File class and some indexing functions. """
    def __init__(self, root, ignore_dirs=[], ignore_files=[], focus_files=[]):
        """ create a file index built out of instances of the File class. """
        logging.debug(ignore_files)
        self.files = []
        for p in self.generate_paths(root, ignore_dirs, ignore_files, focus_files):
            self.append(p)

    def generate_paths(self, root, ignore_dirs=[], ignore_files=[], focus_files=[]):
        """ walk through the file system and yield paths based on the given filters"""
        for r, dirs, fs in os.walk(root):
            dirs[:] = filter(lambda x: x not in ignore_dirs, dirs)
            fs = filter(lambda x: True not in (bool(re.search(p, x)) for p in ignore_files), fs)
            if focus_files:
                fs = filter(lambda x: x in focus_files, fs)
            for f in fs:
                yield os.path.join(r, f)

    def append(self, f):
        _f = fuzzyfile.FuzzyFile(f)
        self.files.append(_f)

    def generate_patterns(self, pattern):
        patterns = []
        for level in range(MATCH_LEVELS):
            segments = [re.escape(x) for x in list(pattern)]
            patterns.append(re.compile(HEAD + CAPTURE.format(level).join(segments) + TAIL))
        return patterns

    def match(self, pattern, include_path=False, list_files=False):
        """ find the best match in the file index for the given pattern. """
        patterns = self.generate_patterns(pattern)
        for f in self.files:
            f.match(patterns, include_path=include_path)  # the fuzzyfile object will update with its scores.

        # return the "best" match, that is the one with the lowest score (fewest interposed characters)
        if True in map(lambda x: bool(x), self.files):
            if list_files:
                return filter(lambda x: bool(x), self.files)
            else:
                return min(self.files)
        elif not include_path:
            return self.match(pattern, include_path=True, list_files=list_files)
        else:
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    FI = FuzzyIndex(os.getcwd())
    for f in FI.files:
        logging.info(f.name)
