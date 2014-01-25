ROOT := .
SRC_DIR := $(ROOT)/fff
TEST_DIR := $(ROOT)/test

install: $(SRC)/*
	python setup.py install

clean:
	python setup.py clean

clean-all: clean
	find . -name "*.pyc" -delete

test: test-fuzzyfile pep8

test-fuzzyfile: $(TEST_DIR)/test_fuzzyfile.py
	python $(ROOT)/test/test_fuzzyfile.py

pep8: *.py
	pep8 . --ignore=E501 --exclude=build
