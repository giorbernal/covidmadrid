#!/bin/bash

DIR=datasets

PRESS_URL=https://github.com/datadista/datasets/raw/master/COVID%2019/ccaa_ingresos_camas_convencionales_uci.csv
PRESS_FILE=$DIR/press.csv

TEST_URL=https://github.com/datadista/datasets/raw/master/COVID%2019/ccaa_covid19_test_realizados.csv
TEST_FILE=$DIR/test.csv

CASES_URL=https://github.com/datadista/datasets/raw/master/COVID%2019/ccaa_covid19_datos_isciii_nueva_serie.csv
CASES_FILE=$DIR/cases.csv

rm -f $PRESS_FILE
rm -f $TEST_FILE
rm -f $CASES_FILE

wget $PRESS_URL --no-check-certificat -O $PRESS_FILE
wget $TEST_URL --no-check-certificat -O $TEST_FILE
wget $CASES_URL --no-check-certificat -O $CASES_FILE
