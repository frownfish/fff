install: src/fff/
	python setup.py -q install

clean:
	python setup.py -q clean

clean-all:
	make clean
	find . -name "*.pyc" -delete

test: test/test_all.py test-fuzzyfile
	python test/test_all.py

test-fuzzyfile: test/test_fuzzyfile.py
	python test/test_fuzzyfile.py
