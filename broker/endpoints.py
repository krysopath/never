from flask_restful import Resource
from .mongodb import make_mongo
from flask_restful import reqparse
from bson.objectid import ObjectId
import base64

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
    def get(self, queried_id):
        client = make_mongo('never', 'never123')
        db = client['neverdb']
        logins = db.logins
        _id = ObjectId(
                base64.standard_b64decode(queried_id)
            )
        return logins.find_one(
            {"_id": _id}
        )

    def delete(self, queried_id):
        client = make_mongo('never', 'never123')
        db = client['neverdb']
        logins = db.logins
        _id = ObjectId(
                base64.standard_b64decode(queried_id)
            )
        logins.delete_one({"_id": _id})
        return _id, 204

    def put(self, queried_id):
        args = parser.parse_args()
        client = make_mongo('never', 'never123')
        db = client['neverdb']
        logins = db.logins
        _id = ObjectId(
                base64.standard_b64decode(queried_id)
            )
        print(args)
        return logins.find_one({'_id': _id}), 201


class TodoList(Resource):
    def get(self):
        client = make_mongo('never', 'never123')
        db = client['neverdb']
        logins = db.logins
        results = [t for t in logins.find()]
        print(results)
        return results, 200

    def post(self):
        args = parser.parse_args()
        client = make_mongo('never', 'never123')
        db = client['neverdb']
        logins = db.logins

        new_id = logins.insert_one( {'task': args['task']}).inserted_id
        return new_id, 201


