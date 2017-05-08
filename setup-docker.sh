#!/bin/bash

# build the flask container
docker build -t jcsesznegi/simple-kanji-viewer .

# create the network
docker network create simple-kanji-viewer

# start the ES container
docker run -dp 9200:9200 --net simple-kanji-viewer --name es elasticsearch

# start the flask app container
docker run -d --net simple-kanji-viewer -p 5000:5000 --name simple-kanji-viewer jcsesznegi/simple-kanji-viewer


