#Fuzzy File Finder
[![Build Status](https://travis-ci.org/frownfish/fff.png?branch=master)](https://travis-ci.org/frownfish/fff)
[![Coverage Status](https://coveralls.io/repos/frownfish/fff/badge.png?branch=master)](https://coveralls.io/r/frownfish/fff?branch=master)
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
Installing the package will allow you to run the fffind function directly from the command line. Run ``` fffind --help ``` for more information.
