import json
from bson.objectid import ObjectId
from datetime import datetime


class ComplexEncoder(json.JSONEncoder):
    """
    Recursively encodes objects if they have toJSON function

    Converts ObjectId and datetime objects to strings

    json.dumps(obj.toJSON(), cls=ComplexEncoder)
    """
    def default(self, obj):
        serializable = {}

        if hasattr(obj, 'toJSON'):
            serializable = obj.toJSON()
        elif isinstance(obj, ObjectId):
            serializable = str(obj)
        elif isinstance(obj, datetime):
            serializable = obj.isoformat()
        else:
            serializable = super(ComplexEncoder, self).default(obj)

        return serializable


def iso_to_datetime(iso_str):
    """
    convert iso strings to datetime objects

    silently fails, returns None if iso_str is invalid
    """
    try:
        iso = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        iso = None

    return iso
