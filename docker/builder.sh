#!/bin/sh 
mkdir -p /code
cd /code
apk add \
  --no-cache \
  --update \
  $BUILD_APKS

pip3 install --upgrade pip 
pip3 install virtualenv 
virtualenv /code/venv 
. /code/venv/bin/activate 
pip3 install -r requirements.txt
