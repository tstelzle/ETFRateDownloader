# MAKEFILE https://github.com/tstelzle/ETFRateDownloader
# AUTHORS: Tarek Stelzle

MOUNT-DIR := $(pwd)
IMAGE-NAME := etf-rate-downloader_image
CONTAINER-NAME := etfRateDownloader

build-image:
	docker build -t $(IMAGE-NAME) .

run:
	docker rm $(CONTAINER-NAME)
	docker run -v $(MOUNT-DIR):/run/ETFRateDownloader/downloads --name $(CONTAINER-NAME) $(IMAGE-NAME)
