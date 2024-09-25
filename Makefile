# test:
# 	pytest
# build:
# 	if [ -d "dist" ]; then rm -rf dist; fi
# 	if [ -d "build" ]; then rm -rf build; fi
# 	if [ -d "prompt_parser.egg-info" ]; then rm -rf prompt_parser.egg-info; fi
# 	pip install setuptools wheel twine 
# 	python setup.py sdist bdist_wheel
# publish_test: build
# 	twine upload --repository testpypi dist/*
# publish_prod: build
# 	twine upload dist/*
# Assumptions:
# 1. You have installed twine wheel and pytest (pip install twine wheel pytest)
# 2. You have created a .pypirc file with your login credentials for both PyPI and testpypi.python.org (see https://packaging.python.org/distributing/#create-an-account)
# 3. You have created a setup.py file with all the usual information (see https://packaging.python.org/distributing/)
# 4. You store the version of your package in a file called "VERSION" in a dir with the same name as $PKG_NAME below (method 4 from https://packaging.python.org/single_source_version/)
# 5. You have a git tag that exactly matches the contents of the "VERSION" file
SHELL=/bin/bash
PYTHON=python3  # Change this to "python" if you're using Python 2
PKG_NAME=prompt_parser  # Change to the name of your package

default: | clean run_tests check_tags bundle register upload
	@echo "Full service complete"

clean:
	@echo "Removing the build/ dist/ and *.egg-info/ directories"
	@rm -rf build dist *.egg-info

check_tags:
	@VER=`cat VERSION`; \
	echo "Making sure that a tag has been created with the correct version number ($$VER)"; \
	TAGS=`git tag -l $$VER`; \
	if echo $$TAGS | grep -q $$VER; then echo "Found tag for version $$VER"; \
	else echo "No git tag '"$$VER"' found. You can create it with the following command:"; \
	echo; echo "git tag $$VER && git push --tags origin"; echo; exit 1; fi

bundle:
	@echo "Bundling the code"; echo
	@${PYTHON} setup.py sdist bdist_wheel

register:
	@echo; echo "Registering this version of the package on PyPI"; echo
	@for bundle in dist/*; do ${PYTHON} `which twine` register $$bundle; done

upload:
	@echo "Uploading built package to PyPI"
	@${PYTHON} `which twine` upload dist/*

run_tests:
	pytest

test_all: | clean run_tests check_tags bundle register_test upload_test
	@echo; echo "Full test complete. Package available on Test PyPI."

register_test:
	@echo; echo "Registering this version of the package on Test PyPI"; echo
	@for bundle in dist/*; do ${PYTHON} `which twine` register $$bundle -r testpypi; done

upload_test:
	@echo; echo "Uploading built package to Test PyPI"
	@${PYTHON} `which twine` upload dist/* -r testpypi
