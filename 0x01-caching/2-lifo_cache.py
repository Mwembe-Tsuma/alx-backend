#!/usr/bin/python3
""" LIFO Cache module"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache inherits from BaseCaching """

    def __init__(self):
        """ Initialize the LIFO Cache """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache using LIFO """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = list(self.cache_data.keys())[-1]
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key"""
        if key is not None:
            return self.cache_data.get(key)
