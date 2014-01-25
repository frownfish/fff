import os

__all__ = ['fuzzyindex', 'fuzzyfile']
__project__ = 'FuzzyFileFinder'
CLI = 'fffind'

IGNORE_DIRS = ['.git', '.svn', 'build']
IGNORE_FILES = [r'\.pyc$', r'^\.bash', r'^\.git', r'^__']

ROOT = os.getcwd()
