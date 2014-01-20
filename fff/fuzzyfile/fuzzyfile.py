import os
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')



class FuzzyFile:
    """ file object to store information. """
    def __init__(self, path):
        """ parse out some data based on the file path. """
        if os.path.exists(path):
            self.ext = os.path.splitext(path)[1].strip('.')
            self.dir, self.name = os.path.split(path)
            self.path = path
            self.score = 0
            self.head = 0
            self.tail = 0
            self.matched = False
        else:
            pass


    def __lt__(self, other):
        if isinstance(other, FuzzyFile):
            if not self:
                # self is not a match
                return False
            elif not other:
                # other is not a match
                return True
            elif self.score != other.score:
                return self.score < other.score
            elif self.head != other.head:
                # if tie, shortest HEAD portion wins
                return self.head < other.head
            elif self.tail != other.tail:
                # if tie, shortest TAIL portion wins
                return self.tail < other.tail
            else:
                # alphabetically
                return self.name < other.name
        else:
            return NotImplemented


    def __nonzero__(self):
        """ evaluate the class instance as a bool, based on self.matched """
        return self.matched


    def match(self, patterns, include_path=False):
        """ try to match the pattern. 'patterns' is a list of compiled regular expressions. """
        for p in patterns:
            if include_path:
                m = p.search(self.path)
            else:
                m = p.search(self.name)
            if m:
                logging.debug(p)
                self.score = sum([len(x) for x in m.groups()[1:-1]])
                self.head = len(m.groups()[1])
                self.tail = len(m.groups()[-1])
                self.matched = True
                logging.debug("p: {0}, g: {1}".format(self.path, m.groups()))
                logging.debug("s: {0}, h: {1}, t: {2}".format(self.score, self.head, self.tail))
                break


if __name__=="__main__":
    f = FuzzyFile("/home/jeff/git/fff/fff/fuzzyfile/fuzzyfile.py")
    print f.name
    print f.ext
    print f.path

