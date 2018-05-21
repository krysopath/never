#!/bin/sh 

DEPS="anakin:dbio:never"

mkdir -p /code
apk add \
  --no-cache \
  --update \
  $BUILD_APKS

pip3 install --upgrade pip 
pip3 install virtualenv 
virtualenv /code/venv 

. /code/venv/bin/activate

CDR="${DEPS}:"
while [ -n "$CDR" ] 
  do CAR=${CDR%%:*} 
    
    cd $CAR
    python3 setup.py install
    cd ..
    
    CDR=${CDR#*:} 
  done
unset CAR CDR


