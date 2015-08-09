import copy
import json

from bson import ObjectId
from datetime import datetime

from service import logger
from service.utils.jsonencoder import ComplexEncoder
from storage.mongo import mongodb


class MongoObject(object):
    data = {}
    collection = 'test'

    def __init__(self, mongo=None):
        now = datetime.utcnow()
        self.data = {
            'created': now,
            'modified': now,
        }

        if mongo:
            self.data = self.fromJSON(mongo)

    @property
    def json_raw(self):
        """
        generate the raw json
        """
        return json.dumps(self.data, cls=ComplexEncoder)

    @property
    def json(self):
        """
        generate cleaned json
        """
        return json.dumps(self.toJSON(), cls=ComplexEncoder)

    @property
    def id(self):
        return self.data.get('_id', None)

    @property
    def created(self):
        return self.data.get('created', '')

    @property
    def modified(self):
        return self.data.get('modified', '')

    @modified.setter
    def modified(self, timestamp):
        self.data['modified'] = timestamp

    def toJSON(self):
        """
        returns a jsonable object

        perform any cleanup here
        """
        data = copy.deepcopy(self.data)
        data['id'] = data.pop('_id')
        return data

    def fromJSON(self, data):
        """
        cleans up the data from a json object
        """
        # clean up id
        if 'id' in data.keys():
            data['_id'] = ObjectId(data.pop('id'))
        else:
            data['_id'] = ObjectId(data['_id'])

        return data

    def save(self):
        """
        saves the list
        """
        saved = False
        now = datetime.utcnow()
        self.modified = now

        if '_id' in self.data.keys():
            # the list needs updating
            ret = mongodb[self.collection].update({'_id': self.data['_id']}, self.data)

            if ret['n']:
                logger.debug('saved existing {} id:{}'.format(self.collection, self.id))
                saved = True
            else:
                logger.debug('failed to save existing {} id:{}'.format(self.collection, self.id))

        else:
            # new list
            ret = mongodb[self.collection].insert(self.data)

            if ret:
                logger.debug('saved new {} id:{}'.format(self.collection, self.id))
                saved = True
            else:
                logger.debug('failed to save new {}'.format(self.collection))

        return saved

    def delete(self):
        deleted = False
        ret = mongodb[self.collection].remove({'_id': self.data['_id']})

        if ret['n']:
            logger.debug('deleted {} id:{}'.format(self.collection, self.id))
            deleted = True
        else:
            logger.debug('failed to delete {} id:{}'.format(self.collection, self.id))

        return deleted

    @classmethod
    def get_by_id(cls, id):
        obj = None
        mongo_obj = mongodb[cls.collection].find_one({'_id': ObjectId(id)})

        if mongo_obj:
            obj = cls(mongo=mongo_obj)
        else:
            logger.debug('did not find {} id:{}'.format(cls.collection, id))

        return obj

    @classmethod
    def count(cls):
        """
        returns the count of documents in the database
        """
        return mongodb[cls.collection].find().count()

    @classmethod
    def create(cls):
        """
        creates, saves, and returns a new objects
        """
        pass
