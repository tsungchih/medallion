ifneq (,$(wildcard ./.env))
  include .env
  export
endif

.PHONY: tests
.DEFAULT_GOAL := help

# Define COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20

# CLI path settings
DAGSTER := $(shell whereis dagster | awk -F : '{print $$2}')
DAGIT := $(shell whereis dagit | awk -F : '{print $$2}')
DAGSTER_DAEMON := $(shell whereis dagster-daemon | awk -F : '{print $$2}')

# Dagster project settings
WORKING_DIR := $(shell pwd)
PROJ_NAME := $(shell poetry version | cut -d ' ' -f 1)
PROJ_VERSION := $(shell poetry version --short)
LIB_NAME := $(shell echo ${PROJ_NAME} | sed -e "s/-/_/g")
PYTEST_DIRS := $(shell ls -d *_tests)

# Dagster-daemon & Dagit runtime environment variables
DAGSTER_HOME := $(WORKING_DIR)
LOCAL_ARTIFACT_STORAGE_BASE_DIR := $(DAGSTER_HOME)/.artifact
SQLITE_RUN_STORAGE_BASE_DIR := $(LOCAL_ARTIFACT_STORAGE_BASE_DIR)/history
SQLITE_EVENT_LOG_STORAGE_BASE_DIR := $(SQLITE_RUN_STORAGE_BASE_DIR)/run
LOCAL_COMPUTE_LOG_MANAGER_BASE_DIR := $(LOCAL_ARTIFACT_STORAGE_BASE_DIR)/storage
SQLITE_SCHEDULE_STORAGE_BASE_DIR := $(LOCAL_ARTIFACT_STORAGE_BASE_DIR)/schedules

# GCP Credentials
# GCP_CREDS_HOME := ~/Documents/projects/gcp-keypairs
# GCP_CREDS_PATH := $(GCP_CREDS_HOME)/privateproject-278208-dagster-learn-admin-impersonate.json

## Show help information
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# Check if a command exists
cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "Forget to run 'poetry shell'???\nERROR: '$(*)' must be installed and available on your PATH."; exit 1)
## Build Python package
build-pkg:
	@python -m build

## Deploy secrets to the local Kubernetes cluster in namespace - dagster
deploy-secrets: cmd-exists-kubectl
	@kubectl --namespace=dagster apply -f k8s/secret-medallion-air-secret-envs.yaml
	@kubectl --namespace=dagster apply -f k8s/secret-medallion-air.yaml

## Build Docker image
docker-build: cmd-exists-docker
	@docker build \
		--build-arg PROJECT_NAME=$(PROJ_NAME) \
		--tag georgelai/$(PROJ_NAME):$(PROJ_VERSION) \
		--file docker/Dockerfile \

## Start a local deployment of Dagster, including Dagit and the dagster-daemon
run-dagster-dev:cmd-exists-dagster
	@DAGSTER_HOME=$(DAGSTER_HOME) \
	 LOCAL_ARTIFACT_STORAGE_BASE_DIR=$(LOCAL_ARTIFACT_STORAGE_BASE_DIR) \
	 SQLITE_RUN_STORAGE_BASE_DIR=$(SQLITE_RUN_STORAGE_BASE_DIR) \
	 SQLITE_EVENT_LOG_STORAGE_BASE_DIR=$(SQLITE_EVENT_LOG_STORAGE_BASE_DIR) \
	 LOCAL_COMPUTE_LOG_MANAGER_BASE_DIR=$(LOCAL_COMPUTE_LOG_MANAGER_BASE_DIR) \
	 SQLITE_SCHEDULE_STORAGE_BASE_DIR=$(SQLITE_SCHEDULE_STORAGE_BASE_DIR) \
	 $(DAGSTER) dev \
	 --working-directory $(WORKING_DIR)/$(LIB_NAME) \
	 --module-name $(LIB_NAME)

## Run pytest to all the packages in the repository
tests: cmd-exists-coverage
	@coverage run -m pytest $(PYTEST_DIRS)
	@coverage report -m

