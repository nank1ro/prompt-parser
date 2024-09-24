build:
	python setup.py sdist
publish test:
	python3 -m twine upload --skip-existing --repository testpypi dist/*
publish prod:
	python3 -m twine upload --skip-existing dist/*
test:
	pytest
