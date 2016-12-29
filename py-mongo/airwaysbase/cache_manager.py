import redis
import json


class CacheManager(object):

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379)
        self.r.flushall()

    def cache_data(self, key, data):

        for item in data:
            item['_id'] = str(item['_id'])

        self.r.set(key, json.dumps(data))

    def get_from_cache(self, key):

        data = self.r.get(key)
        if data:
            return json.loads(data)

    def clear_cache(self, data):

        keys = self.r.keys()
        for key in keys:
            if key in data:
                self.r.delete(key)