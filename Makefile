APP_VERSION := $(shell grep -oP '(?<=^version = ")[^"]*' pyproject.toml)
APP_DIR := asyncstatsd
NPROCS = $(shell grep -c 'processor' /proc/cpuinfo)
MAKEFLAGS += -j$(NPROCS)
PYTEST_FLAGS := --failed-first -x


install:
	poetry install
	test -d .git/hooks/pre-commit || poetry run pre-commit install

test:
	poetry run pytest ${PYTEST_FLAGS}

testloop:
	watch -n 3 poetry run pytest ${PYTEST_FLAGS}

lint-fix:
	poetry run isort --profile black .
	poetry run black ${APP_DIR}

lint-check:
	poetry run flake8 ${APP_DIR}
	poetry run mypy .


rename-project: NEW_APP_DIR :=$(shell echo ${NEW_APP_NAME} | tr '-' '_')
rename-project: APP_NAME := $(shell echo ${APP_DIR} | tr '_' '-')
rename-project:
	@echo "Renaming project ${APP_NAME} to ${NEW_APP_NAME}"
	@echo "Renaming directories ${APP_DIR} to ${NEW_APP_DIR}"
	mv ${APP_DIR} ${NEW_APP_DIR}
	find ./ -type f -not -path "./.git/*" -exec sed -i 's/${APP_DIR}/${NEW_APP_DIR}/g' {} \;
	find ./ -type f -not -path "./.git/*" -exec sed -i 's/${APP_NAME}/${NEW_APP_NAME}/g' {} \;


lint: lint-fix lint-check
