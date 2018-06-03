#!/bin/sh 
apk add \
  --no-cache \
  --update \
  $RUN_APKS

adduser \
  -DS \
  -s /bin/ash \
  -h /code/storage \
  never

mkdir -p /code/storage/stash
chown -R never:nogroup /code 
