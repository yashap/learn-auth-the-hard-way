.DEFAULT_GOAL:=help

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM = 20
APP_IMAGE_NAME = learn_auth_fake_application
APP_CONTAINER_NAME = learn_auth_fake_application

.PHONY: help
## Show this help
help:
	@printf 'Usage:\n  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}\n\n'
	@printf 'Targets:\n'
	@awk '/^[a-zA-Z\-\_\/0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.PHONY: auth/run
## Build and run the Open ID Connect Provider
auth/run:
	docker-compose -f $(ROOT_DIR)/fusion-auth/docker-compose.yml up

.PHONY: auth/open
## Open the Open ID Connect admin page (must be running)
auth/open:
	open http://localhost:9011

.PHONY: app/build
## Build the fake application
app/build:
	docker build -t $(APP_IMAGE_NAME):latest $(ROOT_DIR)/fake-application

.PHONY: app/run
## Run the fake application
app/run:
	docker run --rm --name $(APP_CONTAINER_NAME) -v $(ROOT_DIR)/fake-application/src/app:/usr/src/app -p 8080:5000 $(APP_IMAGE_NAME):latest

.PHONY: app/exec
## Exec into the running app
app/exec:
	docker exec -it $(APP_CONTAINER_NAME) bash

.PHONY: app/open
## Open the app (must be running)
app/open:
	open http://localhost:8080
