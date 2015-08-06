# attempt to unify the mongo initialization
import pymongo


def mongo_client(hosts, database, user='', password=''):
    """
    Returns a pymongo client
    """
    client = pymongo.MongoClient(hosts)
    mongodb = client[database]

    # authenticate
    if all([user, password]):
        mongodb.authenticate(user, password)

    return mongodb


def mongo_factory():
    """
    wraps getting a mongo client reading defaults from the settings
    """
    from settings import config

    hosts = config.get('mongo.hosts', 'localhost:27017')
    database = config.get('mongo.database', 'test')
    user = config.get('mongo.user', '')
    password = config.get('mongo.password', '')
    hosts = hosts.split(',')

    return mongo_client(hosts, database, user, password)


mongodb = mongo_factory()
