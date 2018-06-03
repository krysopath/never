#!/bin/ash
chown never:nogroup /code/storage/stash
exec /bin/ash -c ". /code/venv/bin/activate && /code/run_api.py ${@}"
