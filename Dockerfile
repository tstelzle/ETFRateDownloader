#FROM python:3.9.1-alpine3.13
FROM python:3.12.0b1-alpine3.18

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk
#RUN apk add glibc-2.30-r0.apk
#RUN apk add glibc-bin-2.30-r0.apk

RUN apk add firefox=113.0.2-r1
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /usr/bin

WORKDIR /run/ETFRateDownloader
COPY requirements.txt ./
RUN mkdir -p /run/ETFRateDownloader/downloads
RUN chown -R 1000:1000 /run/ETFRateDownloader/downloads

RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

VOLUME /run/ETFRateDownloader
VOLUME /run/ETFRateDownloader/downloads
VOLUME /run/ETFRateDownloader

ENTRYPOINT ["python", "/run/ETFRateDownloader/main.py"]
