#!/usr/bin/python3
""" LFU Cache module"""


from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache inherits from BaseCaching """

    def __init__(self):
        """ Initialize the LFU Cache """
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """ Add an item in the cache using LFU algorithm """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                hz = min(self.frequency.values())
                candidates = [k for k, v in self.frequency.items() if v == hz]

                if len(candidates) == 1:
                    lfu = candidates[0]
                else:
                    lfu = min(self.cache_data, key=lambda k: self.frequency[k])

                del self.cache_data[lfu]
                del self.frequency[lfu]
                print("DISCARD: {}".format(lfu))

            self.cache_data[key] = item
            self.frequency[key] = self.frequency.get(key, 0) + 1

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.cache_data:
                self.frequency[key] += 1
                return self.cache_data[key]
        return None
