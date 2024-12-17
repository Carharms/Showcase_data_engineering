from functools import lru_cache
import functools
import time

class CacheInfo:
    """
    CacheInfo object used to represent the current status of `lru_cache`
    """

    def __init__(self, max_size):
        self.max_size = max_size
        self.misses = 0
        self.hits = 0
        self.cur_size = 0
        # NOTE: you may add to this if you want, but do not modify the lines above

    def __repr__(self):
        return f"CacheInfo(hits={self.hits}, misses={self.misses}, max_size={self.max_size}, cur_size={self.cur_size})"


def lru_cache(max_size):

    # store initial values in a variable
    cache_info = CacheInfo(max_size)

    # empty LRU cache and time_used list for easy sorting last access
    cache = {}
    time_used = []

    def decorator(func):
        
        def wrapper(*args, **kwargs):

            # unique key to track arguements - the below solves all but arg types
            key = (tuple(str(args)), tuple(str(kwargs.items())))
            
            if key in cache:
                # add to self.hits
                cache_info.hits += 1

                # adjust time_used list to re-position the last 
                time_used.remove(key)
                time_used.append(key)
                return cache[key]
            
            # add to self.misses
            cache_info.misses +=1

            # pop oldest_key from first position in list and reduce self.sur_size
            if cache_info.cur_size >= max_size:
                oldest_key = time_used.pop(0)
                del cache[oldest_key]
                cache_info.cur_size -=1
            
            # if new arg/kwarg cache the result and append to end of time_used list
            result = func(*args, **kwargs)
            cache[key] = result
            time_used.append(key)
            cache_info.cur_size +=1
            return result
        

        wrapper.cache_info = cache_info
        return wrapper
    

    return decorator
        
                        
        