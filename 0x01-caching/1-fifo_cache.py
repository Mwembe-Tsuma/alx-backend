#!/usr/bin/python3
""" FIFO Cache module"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO Cache inherits from BaseCaching"""

    def __init__(self):
        """ Initialize FIFO Cache"""
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache using FIFO algorithm"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = next(iter(self.cache_data))
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key"""
        if key is not None:
            return self.cache_data.get(key)
