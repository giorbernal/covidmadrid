#!/bin/bash

. /opt/app/logger.sh
clearLogs

log 'Initiating data loader daemon ...'
/opt/app/getSourceData.sh &
log 'data loader daemon initiated!'

log 'Initiating application'
/opt/app/setup.sh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export APP_PATH='/opt/app/'
streamlit run $APP_PATH/main.py
