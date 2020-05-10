#!/bin/bash

export LOG_FILE=/var/log/covidmadrid.log
export LOG_DEST=${LOG_DEST:-'stdout'}

function clearLogs {
  rm -fR $LOG_FILE
  touch $LOG_FILE
}

function log {
  DATE=`date`
  if [[ $LOG_DEST == 'stdout' ]]; then
    echo "$DATE - $1"
  else
    echo "$DATE - $1" >> $LOG_FILE
  fi
}
