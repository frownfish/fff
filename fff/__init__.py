import os

__all__ = ['fuzzyindex', 'fuzzyfile']
__project__ = 'FuzzyFileFinder'
CLI = 'fffind'

ROOT = os.getcwd()

IGNORE_DIRS = ['.git', '.svn', 'build']
IGNORE_FILES = [r'\.pyc$', r'^\.bash', r'^\.git', r'^__']
MATCH_LEVELS = 20
CAPTURE = "(.{{,{0}}}?)"
HEAD = "^(?P<head>.*?)"
TAIL = "(?P<tail>.*?)$"
