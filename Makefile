# MAKEFILE https://github.com/tstelzle/ETFRateDownloader
# AUTHORS: Tarek Stelzle

MOUNT-DIR := $(PWD)/downloads
LINK-FILE := $(PWD)/downloads/links.txt
APP-DIR := $(PWD)/app
IMAGE-NAME := etf-rate-downloader_image
CONTAINER-NAME := etfRateDownloader

build-image:
	docker build -t $(IMAGE-NAME) .

run:
	cp $(LINK-FILE) ./app/links.txt
	docker run -v $(MOUNT-DIR):/run/ETFRateDownloader/downloads -v $(APP-DIR):/run/ETFRateDownloader $ --name $(CONTAINER-NAME) --rm $(IMAGE-NAME)
