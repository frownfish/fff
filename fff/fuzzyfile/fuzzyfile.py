import os
import re
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

MATCH_LEVELS = 6

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


    def match(self, pattern):
        """ try to match the pattern """
        # pattern.replace(".", "\\.")
        CAPTURE = "(.{{,{0}}}?)"
        HEAD = "^(.*?)"
        TAIL = "(.*?)$"
        for level in range(MATCH_LEVELS):
            _pat = HEAD + CAPTURE.format(level).join(list(pattern)) + TAIL
            m = re.search(_pat, self.name)
            if m:
                self.score = sum([len(x) for x in m.groups()[1:-1]])
                self.head = len(m.groups()[1])
                self.tail = len(m.groups()[-1])
                self.matched = True
                logging.debug( "p: {0}, g: {1}, s: {2}, h: {3}, t: {4}".format(self.path,
                                                                               m.groups(),
                                                                               self.score,
                                                                               self.head,
                                                                               self.tail))
                break
        



if __name__=="__main__":
    F = FuzzyFile("/home/jeff/git/fff/fff/fuzzyfile/fuzzyfile.py")
    print F.name
    print F.ext
    print F.path

