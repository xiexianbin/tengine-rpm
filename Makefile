DOCKER       = docker
DOCKER_IMAGE = xiexianbin/rpm-builder

COPR_LOGIN = $(shell cat ~/.config/copr | grep login | awk -F ' = ' '{ print $$2 }')
COPR_USERNAME = $(shell cat ~/.config/copr | grep username | awk -F ' = ' '{ print $$2 }')
COPR_TOKEN = $(shell cat ~/.config/copr | grep token | awk -F ' = ' '{ print $$2 }')
COPR_URL = $(shell cat ~/.config/copr | grep copr_url | awk -F ' = ' '{ print $$2 }')

.PHONY: bash build copr debug

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

debug: build bash ## Build Docker image to build rpm and into bash.

build: ## Build Docker image to build rpm.
	$(DOCKER) build -t $(DOCKER_IMAGE) .

bash: ## Run /bin/bash in the Docker image to build rpm.
	@docker run -it \
		--privileged=true \
		-e "COPR_LOGIN=$(COPR_LOGIN)" \
		-e "COPR_USERNAME=$(COPR_USERNAME)" \
		-e "COPR_TOKEN=$(COPR_TOKEN)" \
		-e "COPR_URL=$(COPR_URL)" \
		$(DOCKER_IMAGE) \
		/bin/bash

copr: ## Run docker image to build rpm and push srpm to copr.
	@docker run -it \
		--privileged=true \
		-e "COPR_LOGIN=$(COPR_LOGIN)" \
		-e "COPR_USERNAME=$(COPR_USERNAME)" \
		-e "COPR_TOKEN=$(COPR_TOKEN)" \
		-e "COPR_URL=$(COPR_URL)" \
		$(DOCKER_IMAGE)
