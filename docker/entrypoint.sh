#!/bin/bash

if [ $FLAT_DOCKER = true ]; then
  echo 'blocking execution!'
  sleep 99999999
else
  echo 'Initiating application'
  export LC_ALL=C.UTF-8
  export LANG=C.UTF-8
  export APP_PATH='/opt/app/'
  streamlit run $APP_PATH/main.py
fi