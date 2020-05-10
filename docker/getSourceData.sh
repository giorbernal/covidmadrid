#!/bin/bash

LOG_FILE=/var/log/covidmadrid.log

export MUNI_URL=${MUNI_URL:-'https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/b2a3a3f9-1f82-42c2-89c7-cbd3ef801412/download/covid19_tia_muni_y_distritos.csv'}
export ZONE_URL=${ZONE_URL:-'https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/b7b9edb4-0c70-47d3-9c64-8c4913830a24/download/covid19_tia_zonas_basicas_salud.csv'}
export $POLLING_SOURCE_DATA=${POLLING_SOURCE_DATA:-'28800'}

rm -fR &LOG_FILE
touch &LOG_FILE

function log {
  DATE=`date`
  echo "$DATE - $1" >> $LOG_FILE
}

while true; do
  log 'getting data ...'
  wget $MUNI_URL --no-check-certificat -O /opt/app/datasets/covid19_tia_muni_y_distritos.csv
  wget $ZONE_URL --no-check-certificat -O /opt/app/datasets/covid19_tia_zonas_basicas_salud.csv
  log 'data refreshed!'
  sleep $POLLING_SOURCE_DATA
done
