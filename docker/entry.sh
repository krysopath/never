#!/bin/ash
chown never:nogroup /code/storage/stash
#exec /bin/ash -c ". /code/venv/bin/activate && broker ${@}"
exec /bin/ash -c "sleep 99999"
