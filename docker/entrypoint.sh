#!/bin/bash

echo 'Initiating data loader daemon ...'
/opt/app/getSourceData.sh &
echo 'data loader daemon initiated!'

echo 'Initiating application'
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export APP_PATH='/opt/app/'
streamlit run $APP_PATH/main.py
