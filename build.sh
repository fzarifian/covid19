#!/bin/bash
wget -O chiffres-cles-$( date "+%Y-%m-%d"  ).json https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json 
python3 setup.py build
python3 setup.py install
clear
covid19 data chiffres-cles-$( date "+%Y-%m-%d"  ).json
