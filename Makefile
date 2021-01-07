# MAKEFILE https://github.com/tstelzle/ETFRateDownloader
# AUTHORS: Tarek Stelzle

MOUNT-DIR := $(pwd)
APP-DIR := $(PWD)/app
IMAGE-NAME := etf-rate-downloader_image
CONTAINER-NAME := etfRateDownloader

build-image:
	docker build -t $(IMAGE-NAME) .

run:
	docker run -v $(MOUNT-DIR):/run/ETFRateDownloader/downloads -v $(APP-DIR):/run/ETFRateDownloader $ --name $(CONTAINER-NAME) --rm $(IMAGE-NAME)
