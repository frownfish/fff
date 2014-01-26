import os
import shutil

TEST_ROOT = 'tmp'
PATH_SEP = '/'
NO_MATCH = ' '

FOCUS_FILES = [
    'dir0_file1.ext'
    ]

IGNORE = [
    'dir2/py.pyc',
    'dir2/__init__.py',
    '.git/nomatch.ext'
    ]

FILES = [
    'dir1/dir1_file1.ext',
    'dir1/dir1_file2.ext',
    'dir2/dir2_file1.ext',
    'dir2/dir2_file2.ext',
    ]

BOGUS_FILE = '/home/jeff/bogusfile.txt'
FAKE_FILE = '/home/jeff/otherfile.txt'


def prepend_root(files):
    return [PATH_SEP.join([TEST_ROOT, p]) for p in files]


def setup_file_system(files):
    def makefile(path):
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        open(path, 'a').close()

    for f in files:
        makefile(f)

def cleanup_file_system(root):
    shutil.rmtree(TEST_ROOT)

FOCUS_FILES = prepend_root(FOCUS_FILES)
IGNORE = prepend_root(IGNORE)
FILES = prepend_root(FILES)
FILE_SYSTEM = FILES + IGNORE + FOCUS_FILES
