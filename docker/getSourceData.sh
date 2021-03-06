#!/bin/bash

. /opt/app/logger.sh

export MUNI_URL=${MUNI_URL:-'https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/f22c3f43-c5d0-41a4-96dc-719214d56968/download/covid19_tia_muni_y_distritos_s.csv'}
export ZONE_URL=${ZONE_URL:-'https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/43708c23-2b77-48fd-9986-fa97691a2d59/download/covid19_tia_zonas_basicas_salud_s.csv'}
export STATE_URL=${STATE_URL:-'https://cnecovid.isciii.es/covid19/resources/agregados.csv'}
export POLLING_SOURCE_DATA=${POLLING_SOURCE_DATA:-'28800'}

while true; do
  log 'getting data ...'
  wget $MUNI_URL --no-check-certificat -O /opt/app/datasets/covid19_tia_muni_y_distritos_s.csv
  wget $ZONE_URL --no-check-certificat -O /opt/app/datasets/covid19_tia_zonas_basicas_salud_s.csv
  wget $STATE_URL --no-check-certificat -O /opt/app/datasets/covid19_estado_raw.csv
  cat /opt/app/datasets/covid19_estado_raw.csv | grep -E '^MD,.*|CCAA,.*' > /opt/app/datasets/covid19_estado.csv
  rm -f /opt/app/datasets/covid19_estado_raw.csv
  log 'data refreshed!'
  sleep $POLLING_SOURCE_DATA
done
