import os
import sys
import re
import logging
import multiprocessing
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

import fuzzyfile
from fff import MATCH_LEVELS, CAPTURE, HEAD, TAIL, MAX_WORKERS

nworkers = multiprocessing.Value('i', 0)


class FuzzyIndex:
    """ class to hold isntances of the File class and some indexing functions. """
    def __init__(self, root, exclude_dirs=[], exclude_files=[], focus_files=[]):
        """ create a file index built out of instances of the File class. """
        self.files = []
        for r, dirs, files in os.walk(root):
            # do all the filtering
            dirs[:] = self.filter_dirs(dirs, exclude_dirs)
            files = self.filter_files(files, exclude_files, focus_files)

            # append files to this object
            for f in files:
                self.append(os.path.join(r, f))

            # spawn a subprocess for each dir, if there are more than 2
            if len(dirs) > 1:
                logging.debug('creating subprocess pool')
                pool = multiprocessing.Pool(len(dirs))
                # subdirs = [os.path.join(r, d) for d in dirs]
                kwargs = {'exclude_dirs': exclude_dirs, 'exclude_files': exclude_files, 'focus_files': focus_files}
                while dirs:
                    with nworkers.get_lock():
                        if nworkers.value < MAX_WORKERS:
                            nworkers.value += 1
                        else:
                            break
                    s = os.path.join(r, dirs.pop())
                    pool.apply_async(FuzzyIndex, args=(s,), kwds=kwargs, callback=self.extend)
                pool.close()
                pool.join()

    def filter_dirs(self, dirs, exclude_dirs=[]):
        return filter(lambda x: x not in exclude_dirs, dirs)

    def filter_files(self, files, exclude_files=[], focus_files=[]):
        files = filter(lambda x: True not in (bool(re.search(p, x)) for p in exclude_files), files)
        if focus_files:
            files = filter(lambda x: x in focus_files, files)
        return files

    def extend(self, other):
        if isinstance(other, type(self)):
            logging.debug('extend called')
            self.files.extend(other.files)
        else:
            raise NotImplementedError('extend not defined for type : {}'.format(type(other)))

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
            if list_files:
                return []
            else:
                return None


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    FI = FuzzyIndex(os.getcwd())
    for f in FI.files:
        logging.info(f.name)
