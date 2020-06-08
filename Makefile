DOCKERFILES ?= build/
BUILD_TAG := build
APP_NAME := beaujr/python-ble-detector
REGISTRY := docker.io
GIT_SHORT_COMMIT := $(shell git rev-parse --short HEAD)
IMAGE_TAG ?= 0.1

.PHONY: docker_build

exec:
	@docker run -it --rm --privileged --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host \
        --name=ble --entrypoint=sh \
        -v $(shell pwd)/src:/app \
        $(REGISTRY)/$(APP_NAME):$(BUILD_TAG)

run: | docker_build
	@docker run -it -d --restart=always --privileged --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host \
	--name=ble --entrypoint=python \
	-v $(shell pwd)/src:/app \
	-w /app \
       	$(APP_NAME):$(BUILD_TAG) pizerole.py
	@docker logs -f ble

python-ble-detector:
	@docker run -it -d --restart=always --privileged --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host \
	--name=ble_detector --entrypoint=python \
	-v $(shell pwd)/src:/app \
	-w /app \
	beaujr/python-ble-detector:latest \
	pizerole.py

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
	docker tag $(REGISTRY)/$(APP_NAME):$(BUILD_TAG)-$(ARCH) $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT)-$(ARCH) ; \
	docker push $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT)-$(ARCHTAG);
ifeq ($(GITHUB_HEAD_REF),master)
	docker tag $(REGISTRY)/$(APP_NAME):$(IMAGE_TAG)-$(GIT_SHORT_COMMIT)-$(ARCHTAG) $(REGISTRY)/$(APP_NAME):latest
	docker push  $(REGISTRY)/$(APP_NAME):latest
endif


docker_build:
ifeq ($(GITHUB_HEAD_REF),master)
	docker buildx build \
	--platform linux/$(ARCH) \
	--output "type=image,push=false" \
	--tag $(REGISTRY)/$(APP_NAME):$(BUILD_TAG)-$(ARCHTAG) \
	--file $(DOCKERFILES)/$(DOCKERFILE) $(DOCKERFILES)
else
	docker build \
		-t $(REGISTRY)/$(APP_NAME):$(BUILD_TAG) \
		-f $(DOCKERFILES)/Dockerfile \
		./
endif

docker-login: check-docker-credentials
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS) $(REGISTRY)
