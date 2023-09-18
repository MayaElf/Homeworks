"""
Write a function that accepts another function as an argument. Then it
should return such a function, so the every call to initial one
should be cached.
def func(a, b):
    return (a ** b) ** 2
cache_func = cache(func)
some = 100, 200
val_1 = cache_func(*some)
val_2 = cache_func(*some)
assert val_1 is val_2
"""
from collections.abc import Callable


def cache(func: Callable) -> Callable:
    cached_results = {}

    def wrapper(*args, **kwargs):
        # Convert arguments and keyword arguments to a tuple
        # which can be used as a dictionary key
        key = (args, frozenset(kwargs.items()))
        if key not in cached_results:
            cached_results[key] = func(*args, **kwargs)
        return cached_results[key]

    return wrapper
