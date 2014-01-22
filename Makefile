install: src/fff/
	python setup.py -q install

clean:
	python setup.py -q clean

clean-all:
	make clean
	find . -name "*.pyc" -delete

test: src/fff/*.py
	echo 'why are there no tests yet???'
