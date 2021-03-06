#!/bin/bash

docker run \
	--name=cm1 \
	-p 8501:8501 \
	-d \
	--memory=512m   \
	--memory-swap=-1 \
	-e PORT='8501' \
	-e LOG_DEST='file' \
	-e POLLING_SOURCE_DATA='28800' \
	giorbernal/covidmadrid
