import os
import sys
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from fuzzyfile import fuzzyfile

MATCH_LEVELS = 20
CAPTURE = "(.{{,{0}}}?)"
HEAD = "^(.*?)"
TAIL = "(.*?)$"


class FuzzyIndex:
    """ class to hold isntances of the File class and some indexing functions. """
    def __init__(self, root, ignore_dirs=[], ignore_files=[], focus_files=[]):
        """ create a file index built out of instances of the File class. """
        logging.debug(ignore_files)
        self.files = []
        for r, dirs, fs in os.walk(root):
            for d in ignore_dirs:
                if d in dirs:
                    dirs.remove(d)
            for f in fs:
                if focus_files:
                    if f.lower() in focus_files:
                        path = os.path.join(r, f)
                        self.append(path)
                else:
                    if True not in (bool(re.search(p, f)) for p in ignore_files):
                        path = os.path.join(r, f)
                        self.append(path)


    def append(self, f):
        _f = fuzzyfile.FuzzyFile(f)
        self.files.append(_f)


    def match(self, pattern, include_path=False, list_files=False):
        """ find the best match in the file index for the given pattern. """
        patterns = []
        for level in range(MATCH_LEVELS):
            segments = [re.escape(x) for x in list(pattern)]
            patterns.append(re.compile(HEAD + CAPTURE.format(level).join(segments) + TAIL))
        for f in self.files:
            f.match(patterns, include_path=include_path) # the fuzzyfile object will update with its scores.
        
        # return the "best" match, that is the one with the lowest score (fewest interposed characters)
        if list_files:
            matches = [f for f in self.files if f]
            if matches or (list_files and include_path):
                return matches
            else:
                return self.match(pattern, include_path=True, list_files=list_files)
        else:
            best = min(self.files)  # makes use of the class-defined __lt__ function
            if best:
                return best
            elif not include_path:
                # unsuccessful file name search. expand the search to include the full file paths
                return self.match(pattern, include_path=True, list_files=list_files)
            else:
                return None
            
            


if __name__ == "__main__":
    FI = FuzzyIndex(os.getcwd())
    for f in FI.files:
        logging.debug(f.name)
