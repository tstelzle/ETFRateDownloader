# ETF Rate Downloader

This program downloads '.csv' files for the given ETF`s.
Therefore the website 'https://www.ariva.de/' is used.

## Creating links.txt
For the ETF data you want to download you will have to create a file links.txt.
In there each line is the link to 'historische_kurse' website of the ETF.
So you look up your etf go to 'Kurse' and then to 'Historische Kusre'. 
Copy that link and insert it as a new line into the file links.txt.

## Creating credentials.txt
Ariva.de needs a user to be logged in. so you can download the files. 
Therefore you have to create a file called credentials.txt (see the example credentials.txt.example).
This file has to be put into the app directory, so it will be automatically in the docker container. 

## Running the program
The program runs inside a docker container.
With the given Makefile it is easy to start the docker

The following command will build the image.
```bash
make build-image
```

Afterwards you can run the container with:
```bash
make run 
```
With specifieing a value to MOUNT-DIR you can set the directory in which the files should be downloaded.

For Example:

```bash
make run MOUNT-DIR=/home/test/Desktop
```

will download the .csv files to the Desktop of user test.