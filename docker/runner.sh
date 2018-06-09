#!/bin/ash
chown never:nogroup /code/storage/stash

if test -f /code/migrate_this.db
then
  /bin/ash -c ". /code/venv/bin/activate && /code/migrate_this.py"
else
  echo 'migrating nothing'
fi

exec /bin/ash -c ". /code/venv/bin/activate && /code/run_api.py ${@}"
