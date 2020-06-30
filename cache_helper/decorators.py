try:
    from _pylibmc import Error as CacheSetError
except ImportError:
    from cache_helper.exceptions import CacheHelperException as CacheSetError


from django.core.cache import cache
from django.utils.functional import wraps

from cache_helper import utils

def cached(timeout):

    def _cached(func):
        func_name = utils.get_function_name(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            function_cache_key = utils. get_function_cache_key(func_name, args, kwargs)
            cache_key = utils.get_hashed_cache_key(function_cache_key)

            try:
                value = cache.get(cache_key)
            except Exception:
                value = None

            if value is None:
                value = func(*args, **kwargs)
                # Try and set the key, value pair in the cache.
                # But if it fails on an error from the underlying
                # cache system, handle it.
                try:
                    cache.set(cache_key, value, timeout)
                except CacheSetError:
                    pass

            return value

        def invalidate(*args, **kwargs):
            """
            A method to invalidate a result from the cache.
            :param args: The args passed into the original function. This includes `self` for instance methods, and
            `cls` for class methods.
            :param kwargs: The kwargs passed into the original function.
            :rtype: None
            """
            function_cache_key = utils.get_function_cache_key(func_name, args, kwargs)
            cache_key = utils.get_hashed_cache_key(function_cache_key)
            cache.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper

    return _cached


def cached_class_method(timeout):

    def _cached(func):
        func_name = utils.get_function_name(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # skip the first qarg because it will be the class itself
            function_cache_key = utils. get_function_cache_key(func_name, args[1:], kwargs)
            print(function_cache_key)
            cache_key = utils.get_hashed_cache_key(function_cache_key)

            try:
                value = cache.get(cache_key)
            except Exception:
                value = None

            if value is None:
                value = func(*args, **kwargs)
                # Try and set the key, value pair in the cache.
                # But if it fails on an error from the underlying
                # cache system, handle it.
                try:
                    cache.set(cache_key, value, timeout)
                except CacheSetError:
                    pass

            return value

        def invalidate(*args, **kwargs):
            """
            A method to invalidate a result from the cache.
            :param args: The args passed into the original function. This includes `self` for instance methods, and
            `cls` for class methods.
            :param kwargs: The kwargs passed into the original function.
            :rtype: None
            """
            function_cache_key = utils.get_function_cache_key(func_name, args, kwargs)
            cache_key = utils.get_hashed_cache_key(function_cache_key)
            cache.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper

    return _cached


def cached_instance_method(timeout):

    def _cached(func):
        func_name = utils.get_function_name(func)
        print(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # print(func)
            function_cache_key = utils. get_function_cache_key(func_name, args, kwargs)
            cache_key = utils.get_hashed_cache_key(function_cache_key)

            try:
                value = cache.get(cache_key)
            except Exception:
                value = None

            if value is None:
                value = func(*args, **kwargs)
                # Try and set the key, value pair in the cache.
                # But if it fails on an error from the underlying
                # cache system, handle it.
                try:
                    cache.set(cache_key, value, timeout)
                except CacheSetError:
                    pass

            return value

        return wrapper

    return _cached
