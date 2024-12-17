[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/qI2yGTRS)
# Programming Assignment 3

This assignment provides practice:

* Understanding scope/closure rules. (Problems 1 and 3)
* Implementing a large function by breaking it down into smaller sub-problems on your own without step-by-step guidance. (Problem 1)
* Working with generators (Problem 2).
* Problem 1 also introduces the concept of a `class`.  We will cover classes in detail next week, but you will use a user-defined class (and may, but do not have to, make modifications to it).

## Problem 1 - LRU Cache

Memoization is an optimization technique for speeding up function calls by caching the function result for a given set of inputs.

The standard library provides a decorator `functools.lru_cache` that performs memoization of any function it wraps.
It only stores results from the N most recent calls.  This is called a least recently used (LRU) cache.

For this problem, you will write your own version of `@lru_cache`.

`lru_cache(max_size=128)` should be a decorator that does the following:

- Return the wrapped function with its arbitrary arguments.
- Maintain an LRU cache that stores up to `max_size` arguments and their corresponding results.
    - Function arguments of different types must be cached separately.  For example `f(3)` and `f(3.0)` are distinct calls.
    - The cache must use a LRU policy, a good illustration of this is at
      https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)
    - Add a `cache_info` property to the returned wrapped function object, of type `CacheInfo` below.


### `CacheInfo`

We have provided a class called `CacheInfo`. It has the following public attributes:

- `hits`: Number of calls to the function where the result was returned from the cache.
- `misses`: Number of calls to the function where the result needed to be calculated by calling the function.
- `max_size`: The maximum number of entries the cache can store.
- `cur_size`: The number of entries currently stored.

The class also provide its own string representation for printing.  Here's an example of how `CacheInfo` may be called:

```python
>>> from lru import CacheInfo
>>> cache_info = CacheInfo(max_size=4)
>>> print(cache_info)
CacheInfo(hits=0, misses=0, max_size=4, cur_size=0)
>>> cache_info.hits += 1    # note: class instances are mutable, this is how you would update an attribute
>>> print(cache_info)
CacheInfo(hits=1, misses=0, max_size=4, cur_size=0)
```

You are allowed to add methods/properties to the class to support your implementation, but do not remove/modify what is provided.


### Example
```python

@lru_cache(5)
def add(a, b):
    print(f"add({a}, {b})")
    return a + b

add(1, 2)  # will print add(1, 2)
add(2, 1)  # will print add(2, 1)
add(2, 2)  # will print add(2, 2)
add(1, 2)  # will return 3 without printing, since the cache will be used

print(add.cache_info)
# will print CacheInfo(hits=1, misses=3, max_size=5, cur_size=3)

# make 10 additional calls
for x in range(10):
    add(x, x)

# will again print add(1, 2)
add(1, 2)
# because prior 10 calls will have bumped add(1, 2) from the LRU cache
```

### Hints

* This is a large function, the most complex you've written so far for this class. The key to tackling a problem like this is to break it down into smaller pieces.  Write helper functions as needed (e.g. how will you determine a cache key for a set of args/kwargs?). This will both help you get started with a large task and ensure your design grade remains high.
* There is an implementation in `functools.lru_cache` that is highly optimized and in no way resembles the intended solution for this course. Your implementation **SHOULD NOT** be based on the one that Python provides. (example: your implementation **must** use a dictionary, and not a list for storing the cache)
* You can assign attributes to a function, since functions are objects. (e.g. `my_func.cache_info = CacheInfo(...)`)

To run the tests for this problem: `uv run pytest lru`

## Problem 2 - `sample`

There are many reasons it can be useful to obtain a random sample of data, and for this problem we'll implement a function that helps us do just that from an iterable of unknown size.

To do this we'll implement the function `sample` with the following definition:

```
def sample(items, number, rate=0.2):
    pass
```

- `items` is an iterable. It may be any type of iterable, including a generator.
- `number` is a number of items to collect for the sample.
- `rate` is a floating point number indicating the sample rate.

The function should observe items one at a time from `items`, with a `rate` probability of returning any given item. (By default: 20%)

It should cease once `number` items have been returned.

**You must implement sample as a generator function.  It must not return a list.**


```python
>>> import sample

# your output will vary
>>> for item in sample.sample(range(100), 5):
...     print(item)
4
5
9
13
22

>>> for item in sample.sample(range(100), 5, 1.0):     # sample 100%
...     print(item)
0
1
2
3
4
```


### Special Cases

- If the iterable runs out of items before the specified number of items is returned, the function should exit without error.  (So, for example, 5 items requested from a 10 item list with a low sample rate will likely only return 2-3 items.)
- If 0 items are requested or the sample rate is 0 the correct behavior is to return an empty list. **You should generally not need to implement special logic for this behavior to work.**

### Testing Randomness

Since this function relies on randomness, it can seem difficult to test.

What we do in these situations is set a random seed which results in a predictable stream of random numbers so that our test can behave the same from system to system, run to run.

See `test_sample.py` if you'd like to learn more.

To run the tests for this problem: `uv run pytest sample`

## Problem 3 - `scope_check`

Let's implement a function `scope_check` that helps us understand what is currently happening in our scope.

To do this, open the file `scope_check` and complete the two helper functions within:

### `clean_dict`

There are a lot of variables that start with `_` that clutter up our scope, these might be defined by Python itself or various functions & libraries we are using.  The `clean_dict` function should implement a dictionary comprehension that returns a dictionary without any keys that start with `'_'`.

### `find_conflicts`

This function is used by `sc` to check which locals are shadowing global variables.

Read the docstring for details on what it should return and implement it.

To run the tests for this portion: `uv run pytest scope_check`

### Final Step

You now have a function `sc` that you can call to see the scope of outer functions.

Try running the program to see a demo of this in action:

```
uv run python3 scope_check/scope_check.py
                                  scope_check.py line 91                                  
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ name              ┃ value                       ┃ type   ┃ global?                     ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ a                 │ 1                           │ int    │                             │
│ b                 │ 2                           │ int    │                             │
│ x                 │ 3                           │ int    │ global x is a string        │
│ y                 │ 4                           │ int    │                             │
│ z                 │ this is a long stringthis … │ str    │                             │
└───────────────────┴─────────────────────────────┴────────┴─────────────────────────────┘
```

Note that the parameters `a` and `b` are indeed local scope, that's easily forgotten when considering what is in scope.

The implementation of this function is complex (and beyond what is reasonably covered in our course) but you can take a look at the comments to better understand it.

You can keep this file and import it in other work if you find it useful.
