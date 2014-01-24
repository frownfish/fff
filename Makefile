ROOT := .

install: src/*
	python setup.py install

clean:
	python setup.py clean

clean-all: clean
	find . -name "*.pyc" -delete

test: $(ROOT)/test/test_all.py pep8
	python $(ROOT)/test/test_all.py

test-fuzzyfile: $(ROOT)/test/test_fuzzyfile.py
	python $(ROOT)/test/test_fuzzyfile.py

pep8: *.py
	pep8 . --ignore=E501 --exclude=build
