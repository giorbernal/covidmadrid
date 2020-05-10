#!/bin/bash

echo 'Initiating application'
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export APP_PATH='/opt/app/'
streamlit run $APP_PATH/main.py
