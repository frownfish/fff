ROOT := .
PACKAGE := $(ROOT)/fff
TESTS := $(ROOT)/test
PYTHON := python
PIP := pip
PEP8 := pep8
PEP_IGNORE := E501

# Install ####################################################################

.PHONY: all
all: 
	$(MAKE) install
	$(MAKE) clean-all
	$(MAKE) test

.PHONY: install
install: $(PACKAGE) .depends
	$(PYTHON) setup.py install

.PHONY: .depends
.depends:
	$(PIP) install pep8

# Clean-up ###################################################################

.PHONY: .clean-dist
.clean-dist:
	rm -rf dist build *.egg-info 

.PHONY: clean
clean:
	$(PYTHON) setup.py clean
	find $(PACKAGE) -name "*.pyc" -delete

.PHONY: clean-all
clean-all: clean .clean-dist

# Test #######################################################################

test: $(PACKAGE) test-fuzzyfile pep8

test-fuzzyfile: $(TESTS)/test_fuzzyfile.py
	$(PYTHON) $(ROOT)/test/test_fuzzyfile.py

# Static Analysis ############################################################

.PHONY: pep8
pep8: $(PACKAGE)
	pep8 $(PACKAGE) --ignore=$(PEP_IGNORE)
