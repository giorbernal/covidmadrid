#!/bin/bash

DIR=datasets

MUNI_URL=https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/f22c3f43-c5d0-41a4-96dc-719214d56968/download/covid19_tia_muni_y_distritos_s.csv
MUNI_FILE=$DIR/covid19_tia_muni_y_distritos_s.csv

ZONES_URL=https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/43708c23-2b77-48fd-9986-fa97691a2d59/download/covid19_tia_zonas_basicas_salud_s.csv
ZONES_FILE=$DIR/covid19_tia_zonas_basicas_salud_s.csv

rm -f $MUNI_FILE
rm -f $ZONES_FILE

wget $MUNI_URL --no-check-certificate --no-cache -O $MUNI_FILE
wget $ZONES_URL --no-check-certificate --no-cache -O $ZONES_FILE
