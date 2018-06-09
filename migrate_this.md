if you migrate from the old db backend and still have a table like this:

```
CREATE TABLE logins (_id INTEGER PRIMARY KEY AUTOINCREMENT, _login TEXT NOT NULL, _group TEXT NOT NULL, _link TEXT NOT NULL, _username TEXT NOT NULL, _email TEXT NOT NULL, _notes TEXT NOT NULL, _seed TEXT NOT NULL, _length INTEGER NOT NULL);
```

you can dump it into a sqlite db file named `migrate_this.db` and place it here.
it will be migrated on never launch
