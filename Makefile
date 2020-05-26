TAG ?= ble
.PHONY: build
DIR ?= /home/pi/tuya

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
