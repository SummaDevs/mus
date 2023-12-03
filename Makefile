# requires python 3.11

ifeq ($BUILD_ENV, production)
	SOURCE_ENV=production
else
	ifeq ($BUILD_ENV, develop)
		SOURCE_ENV=develop
	endif
endif

# default target is to show help
help:
	@echo "make help              - print target list"
	@echo "make venv_create       - create virtual environment"
	@echo "make venv_packages     - install dependencies to virtual environment"
	@echo "make venv_dev_packages - install dev dependencies to virtual environment"
	@echo "make venv_clean        - remove virtual environment"
	@echo "make venv_build        - create virtual environment and install dependencies"
	@echo "make venv_dev_build    - create virtual environment and install dev dependencies"
	@echo
	@echo "make run_venv_code_check - run codestyle check using virtual environment"
	@echo "make run_venv_test       - run tests using virtual environment"
	@echo
	@echo "make docker_build  - build docker image"
	@echo "make docker_run    - build docker image"
	@echo
	@echo "make build - default CI/CD build"
	@echo "make test - default CI/CD test"
	@echo "make deploy - default CI/CD deploy"

venv_create:
	@echo ----- Creating virtual environment - local -----
	virtualenv -p python3.11 .venv

venv_packages:
	@echo ----- Installing dependencies to virtual environment -----
	.venv/bin/pip install -r requirements/requirements.txt

venv_dev_packages:
	@echo ----- Installing develop dependencies to virtual environment -----
	.venv/bin/pip install -r requirements/requirements_dev.txt

venv_clean:
	@echo ----- Removing virtual environment - local -----
	rm -rf .venv

venv_build: venv_create venv_packages
venv_dev_build: venv_create venv_dev_packages

run_venv_code_check:
	@echo ----- Run code style checks - local -----
	.venv/bin/pylint app*
	.venv/bin/mypy app*

run_venv_test:
	@echo ----- Run tests - local -----
	.venv/bin/pytest --version
	.venv/bin/pytest -rfs

docker_build:
	@echo ----- Build docker image -----
	docker build . -t api-skeleton-fastapi:latest

docker_run:
	@echo ----- Run docker image -----
	docker run -e SOURCE_ENV=${SOURCE_ENV} api-skeleton-fastapi:latest

# default targets
build:
	@echo ----- CI/CD default build -----
	@echo ----- placeholder - no tasks -----

test: build
	@echo ----- CI/CD default tests -----
	@echo ----- placeholder  - no tasks -----

deploy: build test
	@echo ----- CI/CD default code check -----
	@echo ----- placeholder -----

.PHONY: help \
		venv_create \
		venv_packages \
		venv_dev_packages \
		venv_clean \
		venv_build \
		venv_dev_build \
		run_venv_code_check \
		run_venv_test \
		docker_build \
		docker_run \
		build \
		test \
		deploy
