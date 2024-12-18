## LRU Cache

- `lru_cache(max_size=128)` is be a decorator that:
    - Returns the wrapped function with its arbitrary arguments.
    - Maintains an LRU cache that stores up to `max_size` arguments and their corresponding results.
    
### `CacheInfo`

- a class with the following public attributes:
    - `hits`: Number of calls to the function where the result was returned from the cache.
    - `misses`: Number of calls to the function where the result needed to be calculated by calling the function.
    - `max_size`: The maximum number of entries the cache can store.
    - `cur_size`: The number of entries currently stored.



