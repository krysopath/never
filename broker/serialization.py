import json
from bson.objectid import ObjectId
import base64
from uuid import UUID


class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return {
                "_type": "bson.objectid.ObjectId",
                "b64_binary": base64.b64encode(obj.binary).decode(),
                "string": str(obj),
                "generation_time": obj.generation_time.timestamp()
            }
        elif isinstance(obj, UUID):
            return {
                "_type": "uuid.UUID",
                "uuid": str(obj)
            }


        return super(MongoEncoder, self).default(obj)

