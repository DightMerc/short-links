from django.conf import settings
import logging

import redis
import time


class RedisCache():

    """
    Redis based Cache machine

    set(key, value) - create or update key with value.
    get(key) - get value by selected key.
    delete(key) - delete selected key. 
    """

    def __init__(self):
        self.engine = redis.Redis(
            host=settings.REDIS_HOST,
            db=settings.REDIS_DB
            )

    def set(self, key, value):
        self.engine.mset({key: value})

    def get(self, key):
        try:
            return self.engine.get(key).decode("utf-8")
        except Exception as e:
            return ''

    def delete(self, key):
        self.engine.delete(key)
