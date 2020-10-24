#!/bin/bash

./getData.sh

rm -fR data/covid19_CCAA.csv

python createDataSet.py
