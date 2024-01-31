#!/usr/bin/python3
""" MRU Cache module """


from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache inherits from BaseCaching """

    def __init__(self):
        """ Initialize the MRUCache """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using MRU """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.order.pop()
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))
            self.cache_data[key] = item
            self.order.append(key)
        else:
            return None

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.cache_data:
                self.order.remove(key)
                self.order.append(key)
                return self.cache_data[key]
        return None
