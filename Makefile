DOCKERFILES ?= build/
BUILD_TAG := build
APP_NAME := beaujr/python-ble-detector
REGISTRY := docker.io
GIT_SHORT_COMMIT := $(shell git rev-parse --short HEAD)
IMAGE_TAG ?= 0.1

.PHONY: build

build:
	@docker build -t $(TAG) -f build/Dockerfile build/

exec:
	@docker run -it --rm --privileged --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host \
        --name=ble --entrypoint=sh \
        -v $(shell pwd)/src:/app \
        $(TAG)

run: | build
	@docker run -it -d --restart=always --privileged --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host \
	--name=ble --entrypoint=python \
	-v $(shell pwd)/src:/app \
	-w /app \
       	$(TAG) pizerole.py
	@docker logs -f $(TAG)

check-docker-credentials:
ifndef DOCKER_USER
	$(error DOCKER_USER is undefined)
else
  ifndef DOCKER_PASS
	$(error DOCKER_PASS is undefined)
  endif
endif

docker_push: docker-login
	set -e; \
	docker tag $(REGISTRY)/$(APP_NAME):$(BUILD_TAG) $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT) ; \
	docker push $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT);
ifeq ($(GITHUB_HEAD_REF),master)
	docker tag $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT) $(REGISTRY)/$(APP_NAME):latest
	docker push  $(REGISTRY)/$(APP_NAME):latest
endif

docker_build:
	docker build \
		-t $(REGISTRY)/$(APP_NAME):$(BUILD_TAG) \
		-f $(DOCKERFILES)/Dockerfile \
		./

docker-login: check-docker-credentials
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS) $(REGISTRY)
