#!/usr/bin/env python
import sys
import time
import pickle
import pymongo
import redis


# connect to redis & mongodb
redis_client = redis.Redis()
mongo_client = pymongo.MongoClient()
mongodb = mongo_client['test']['benchmark']
# mongodb.ensure_index('key', unique=True)


def mongo_set(data):
    for k, v in data.iteritems():
        mongodb.insert({'_id': k, 'value': v})


def mongo_get(data):
    for k in data.iterkeys():
        val = mongodb.find_one({'_id': k}, fields=('value',)).get('value')


def redis_set(data):
    for k, v in data.iteritems():
        redis_client.set(k + ':string', v)


def redis_get(data):
    for k in data.iterkeys():
        val = redis_client.get(k + ':string')


def redis_pickle_set(data):
    for k, v in data.iteritems():
        redis_client.set(k + ':pickle', pickle.dumps(v))

def redis_pickle_get(data):
    for k in data.iterkeys():
        val = pickle.loads(redis_client.get(k + ':pickle'))


def do_tests(num, tests):
    # setup dict with key/values to retrieve
    data = {'key:%s' % i: 'val:%s' % i for i in range(num)}

    # run tests
    for test in tests:
        start = time.time()
        test(data)
        elapsed = time.time() - start
        print "Completed %s: %d ops in %.2f seconds : %.1f ops/sec" % (test.__name__, num, elapsed, num / elapsed)


if __name__ == '__main__':
    num = 10000 if len(sys.argv) == 1 else int(sys.argv[1])
    tests = [mongo_set, mongo_get, redis_set, redis_get, redis_pickle_set, redis_pickle_get] # order of tests is significant here!
    do_tests(num, tests)
