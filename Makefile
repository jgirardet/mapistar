.PHONY: build

MODULE:=mapistar

all: dev style doc test test-coverage


install:
	poetry install

devtools:
	pip install ipython pdbpp

dev: devtools install

style: isort black flake8

isort:
	isort -y

black:
	black -q $(MODULE)

flake8:
	flake8

test:
	poetry run pytest

pdb:
	poetry run pytest pdb

test-coverage:
	poetry run py.test  --cov $(MODULE) --cov-report term-missing --cov-report html


push:
	git status
	git push origin --all
	git push origin --tags

doc:
	poetry run make -C docs html

doc-auto:
	poetry run sphinx-autobuild docs docs/_build
	
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name 'requirements*' -exec rm -f {} +
	rm -rf docs/_build/



clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -rf .pytest_cache/


migrate: migrations
	pipenv run apistar migrate

migrations:
	pipenv run apistar makemigrations

run:
	poetry run python manage.py --settings=config.local

shell:
	poetry run ipython --settings=config.local


