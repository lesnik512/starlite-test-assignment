## Local environment commands:
## ---------------------------------------------------------------

.DEFAULT_GOAL := run_tests

## run:       start app in docker
run:
	alembic upgrade head
	uvicorn app.main:app --reload

## pytest:    run pytest (with down/up migrations before)
pytest:
	alembic downgrade base
	alembic upgrade head
	IS_TESTING="TRUE" pytest -s -vv -x tests/

## run_tests: run isort, black, pylint, mypy, pytest
run_tests:
	isort -c --diff --settings-file .isort.cfg .
	black --config pyproject.toml --check .
	pylint --rcfile=.pylintrc --errors-only app
	mypy .
	alembic downgrade base
	alembic upgrade head
	IS_TESTING="TRUE" pytest -s -vv tests/

## migration: create alembic migration
migration:
	alembic revision --autogenerate

## upgrade:   downgrade alembic migrations
upgrade:
	alembic upgrade head

## downgrade: downgrade alembic migrations
downgrade:
	alembic downgrade base

## ---------------------------------------------------------------
## Requirements managing: pip-tools required to be installed and
## pip-compile command required to be available
## ---------------------------------------------------------------

## pip-compile: compile all requirements
# https://github.com/jazzband/pip-tools/issues/1092#issuecomment-632584777
pip-compile: prepare-constraints
	pip-compile constraints.in
	pip-compile requirements.in
	pip-compile requirements.dev.in

## pip-upgrade: upgrade all requirements
pip-upgrade: prepare-constraints
	rm -f constraints.txt requirements.txt requirements.dev.txt
	touch constraints.txt
	pip-compile constraints.in
	pip-compile requirements.in
	pip-compile requirements.dev.in

prepare-constraints: check-pip-compile
	rm -f constraints.in
	touch constraints.txt
	cat requirements.*.in > constraints.in

## pip-sync:    sync requirements in local environment
pip-sync: check-pip-compile
	pip-sync requirements.txt requirements.dev.txt

check-pip-compile:
	@which pip-compile > /dev/null

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
