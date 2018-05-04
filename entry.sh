#!/bin/ash
chown never:nogroup /code/storage/stash
exec /bin/ash -c ". ../venv/bin/activate && broker ${@}"
