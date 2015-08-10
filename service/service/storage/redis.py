from __future__ import absolute_import
import redis
import pickle

from sha import sha
from service import logger


class RedisClient(object):
    type = ''
    _redis = None
    _prefix = ''
    _pickle_token = 'pickle:'
    _timeout = 300

    def __init__(self, host, port, redis_type='cache', password='', prefix='', timeout=300):
        self.type = redis_type
        self._redis = redis.Redis(host, port, password=password, socket_timeout=2)
        self._prefix = prefix
        self._timeout = timeout

    def _tokenize(self, key, hash=False):
        # hash the key if requested
        if hash:
            hashed_key = sha(key).hexdigest()
            key_token = '%s:%s' % (self._prefix, hashed_key)
        else:
            key_token = '%s:%s' % (self._prefix, key)

        return key_token


class RedisCache(RedisClient):
    """
    Redis cache wrapper
    """
    def get(self, key):
        key_token = self._tokenize(key)
        value = None
        stored_value = self._redis.get(key_token)

        if stored_value:
            # check if the stored value is pickled
            if stored_value.find(self._pickle_token) == 0:
                pickled_value = stored_value.replace(self._pickle_token, '', 1)
                value = pickle.loads(pickled_value)
            else:
                value = stored_value

            logger.debug('Got cache key:%s' % key_token)
        else:
            logger.debug('Failed to get cache key:%s' % key_token)

        return value

    def keys(self, pattern):
        pattern_token = self._tokenize(pattern)
        keys = self._redis.keys(pattern_token)

        logger.debug('Got keys for pattern:%s' % pattern_token)
        return keys

    def set(self, key, value):
        key_token = self._tokenize(key)

        # if value is not string then pickle it
        if isinstance(value, basestring):
            stored_value = value
        else:
            pickled_value = pickle.dumps(value)
            stored_value = '%s%s' % (self._pickle_token, pickled_value)

        # set default timer, ignore if not set
        if self._timeout:
            response = self._redis.setex(key_token, stored_value, self._timeout)
        else:
            response = self._redis.set(key_token, stored_value)

        logger.debug('Set cache key:%s' % key_token)
        return response

    def setex(self, key, value, seconds):
        key_token = self._tokenize(key)

        # if value is not string then pickle it
        if isinstance(value, basestring):
            stored_value = value
        else:
            pickled_value = pickle.dumps(value)
            stored_value = '%s%s' % (self._pickle_token, pickled_value)

        response = self._redis.setex(key_token, stored_value, seconds)
        logger.debug('Set cache key:%s' % key_token)
        return response

    def delete(self, *keys):
        key_tokens = [self._tokenize(key) for key in keys]
        response = self._redis.delete(*key_tokens)

        for key_token in key_tokens:
            logger.debug('Delete cache key:%s' % key_token)

        return response

    def delete_pattern(self, pattern):
        """
        deletes all keys that matches the pattern
        """
        key_tokens = self.keys(pattern)

        if key_tokens:
            response = self._redis.delete(*key_tokens)
        else:
            response = True

        for key_token in key_tokens:
            logger.debug('Delete cache key:%s' % key_token)

        return response


class RedisDumyCache(object):
    """
    Dumy redis cache replacement
    """
    def __init__(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return None

    def keys(self, *args, **kwargs):
        return []

    def set(self, *args, **kwargs):
        return False

    def setex(self, *args, **kwargs):
        return False

    def delete(self, *args, **kwargs):
        return False

    def delete_pattern(self, *ags, **kwargs):
        return False


class RedisQueue(RedisClient):
    """
    A simple queue for redis
    """
    @property
    def is_empty(self, key):
        """
        check to see if the queue is empty
        """
        return self.size(key) == 0

    def push(self, key, value):
        """
        add a new element to the end of the queue
        """
        key_token = self._tokenize(key)
        return self._redis.rpush(key_token, value)

    def pop(self, key, block=True, timeout=None):
        """
        remove element from queue, block if true
        """
        key_token = self._tokenize(key)

        if block:
            item = self._redis.blpop(key_token, timeout=timeout)
        else:
            item = lpop(key_token)

        return item

    def size(self, key):
        key_token = self._tokenize(key)
        self._redis.llen(key_token)


class RedisDumyQueue(object):
    is_empty = True

    def __init__(self, *args, **kwargs):
        pass

    def push(self, *args, **kwargs):
        return False

    def pop(self, *args, **kwargs):
        return None

    def size(self, *args, **kwargs):
        return 0


def redis_factory(redis_type):
    from settings import config

    if redis_type == 'cache':
        host = config.get('redis.host', 'localhost')
        port = int(config.get('redis.port', 6379))
        password = config.get('redis.password', '')
        prefix = config.get('redis.prefix', '')
        active = config.get('redis.active', 'false')
        timeout = config.get('redis.timeout', 300)

        if active == 'true':
            redis_client = RedisCache(host, port, redis_type=redis_type, password=password, prefix=prefix, timeout=timeout)
        else:
            redis_client = RedisDumyCache(host, port, redis_type=redis_type, password=password, prefix=prefix, timeout=timeout)

    elif redis_type == 'queue':
        host = config.get('redis_queue.host', 'localhost')
        port = int(config.get('redis_queue.port', 6379))
        password = config.get('redis_queue.password', '')
        prefix = config.get('redis_queue.prefix', '')
        active = config.get('redis_queue.active', 'false')

        if active == 'true':
            redis_client = RedisQueue(host, port, redis_type=redis_type, password=password, prefix=prefix)
        else:
            redis_client = RedisDumyQueue(host, port, redis_type=redis_type, password=password, prefix=prefix)

    return redis_client


redis_cache = redis_factory('cache')
redis_queue = redis_factory('queue')
