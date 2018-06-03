from pymongo import MongoClient
from uuid import uuid4
from urllib.parse import quote_plus


def make_mongo(user='', passw='',
               host='127.0.0.1',
               port=27017,
               db='neverdb'):
    return MongoClient(
        'mongodb://{}:{}@{}:{}/{}'.format(
            quote_plus(user),
            quote_plus(passw),
            host,
            port,
            db,
        )
    )

client = make_mongo('never', 'never123')

snippet = {
    'uuid': uuid4(),
    'name': 'test',
    'group': 'work',
    'username': 'test',
    'email': 'test@org',
    'link': 'mail.org',
    'notes': 'bla',
    'length': 64
}
