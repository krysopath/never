
from flask import Flask, make_response
from flask_restful import abort, Api
from . import endpoints as ep
from .serialization import MongoEncoder
from json import dumps

app = Flask(__name__)
api = Api(app)

settings = app.config.get('RESTFUL_JSON', {})
settings.setdefault('indent', 2)
settings.setdefault('sort_keys', True)
app.config['RESTFUL_JSON'] = settings


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(
        dumps(
            data,
            cls=MongoEncoder,
            indent=2
        ),
        code
    )
    resp.headers.extend(headers or {})
    return resp



def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))



api.add_resource(ep.TodoList, '/logins/')
api.add_resource(ep.Todo, '/logins/<queried_id>')
