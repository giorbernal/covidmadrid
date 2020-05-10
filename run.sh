#!/bin/bash

docker run \
	--name=cm1 \
	-p 8501:8501 \
	-it \
	-e FLAT_DOCKER=true \
	--memory=1g \
	--memory-swap=-1 \
	giorbernal/covidmadrid
