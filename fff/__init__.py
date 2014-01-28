import os

# package info
__all__ = ['fuzzyindex', 'fuzzyfile']
__project__ = 'fff'
__version__ = '0.0.1b'
CLI = 'fffind'

# defaults
MAX_WORKERS = 8
ROOT = os.getcwd()
EXCLUDE_DIRS = ['.git', '.svn', 'build']
EXCLUDE_FILES = [r'\.pyc$', r'^\.bash', r'^\.git', r'^__']
MATCH_LEVELS = 20
CAPTURE = "(.{{,{0}}}?)"
HEAD = "^(?P<head>.*?)"
TAIL = "(?P<tail>.*?)$"
