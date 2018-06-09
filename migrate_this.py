#!/usr/bin/env python3
import sqlite3
from pprint import pprint
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


con = sqlite3.connect("/code/migrate_this.db")
#con.row_factory = sqlite3.Row
con.row_factory = dict_factory
cur = con.cursor()
cur.execute("select * from logins;")

results = cur.fetchall()

to_mongo = []
for r in results:
    to_mongo.append({k.replace('_', ''): v for k, v in r.items()})

from broker import mongodb

db = mongodb.client['neverdb']

db.logins.insert_many(to_mongo)

