#Fuzzy File Finder

##Installation

Clone this repo into a location on your file system.

```git clone https://github.com/frownfish/fff.git```

Change directories to the cloned location.

```cd fff```

Install the package.

```make install```

###Testing the Installation
The testing configuration uses pep8 for static analysis. Install this program using pip.

```pip install pep8```

Run the package test suite as well as static analysis using

```make test```


##Package Contents
###fuzzzyfile
Class to handle pattern matching 

###fuzzyindex
Class to handle traversing the filesystem and storing a list of FuzzyFile object.

###fffind.py
Script that will search the filesystem for files that match the given pattern. 

####Usage
```
usage: fffind.py [-h] [-r ROOT] [-f [FOCUS [FOCUS ...]]]
                 [-if [IGNORE_FILES [IGNORE_FILES ...]]]
                 [-id [IGNORE_DIRS [IGNORE_DIRS ...]]] [-l]
                 pattern

positional arguments:
  pattern               Pattern to match based on. Does not understand regex
                        so don't try :).

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  Top-level directory from which to scan.
  -f [FOCUS [FOCUS ...]], --focus [FOCUS [FOCUS ...]]
                        Limit the search to these files.
  -if [IGNORE_FILES [IGNORE_FILES ...]], --ignore-files [IGNORE_FILES [IGNORE_FILES ...]]
                        Ignore files that match the given patterns
  -id [IGNORE_DIRS [IGNORE_DIRS ...]], --ignore-dirs [IGNORE_DIRS [IGNORE_DIRS ...]]
                        Do not scan into the given directory names
  -l, --list            List all of the matched files instead of picking the
                        'best' one.

```
