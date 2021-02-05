from django.conf import settings
import logging

import redis
import time
logger = logging.getLogger(__name__)


class RedisCache():

    def __init__(self):
        self.engine = redis.Redis(
            host=settings.REDIS_HOST,
            db=settings.REDIS_DB
            )

    def set(self, key, value):
        logger.error(f'set: {key}:{value}')
        self.engine.mset({key: value})

    def get(self, key):
        try:
            return self.engine.get(key).decode("utf-8")
        except Exception as e:
            return ''

    def delete(self, key):
        self.engine.delete(key)
