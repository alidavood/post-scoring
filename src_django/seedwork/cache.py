from django.core.cache import cache


class CacheHelper:
    @staticmethod
    def add(key, value, interval=300):
        cache.set(key, value, interval)

    @staticmethod
    def get(key):
        return cache.get(key)

    @staticmethod
    def get_and_delete(key):
        data = cache.get(key)
        cache.delete(key)
        return data

    @staticmethod
    def delete(key):
        return cache.delete(key)
