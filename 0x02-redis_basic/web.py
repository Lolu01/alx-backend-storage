#!/usr/bin/env python3
"""
This module provides a decorator to count method calls
using Redis and a function to fetch web page content.
"""
import requests
import redis
from typing import Callable
from functools import wraps


redis_instance = redis.Redis()


def cache_data(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method using Redis
    and caches the result for a specific period.
    """
    @wraps(method)
    def inc(url: str) -> str:
        """
        Increments the value of a Redis key and then calls the given method
        Caches the result of the method for a certain period.
        """
        count_key = f"count:{url}"
        result_key = f"result:{url}"
        expiration_time = 10
        redis_instance.incr(count_key)
        cached_content = redis_instance.get(result_key)
        if cached_content:
            print(f"Cache hit for {url}")
            return cached_content.decode('utf-8')

        print(f"Fetching new content for {url}")
        content = method(url)
        redis_instance.setex(result_key, expiration_time, content)
        return content
    return wrapper


@cache_data
def get_page(url: str) -> str:
    """
    Fetches the content of the given URL and returns it as a string.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"

    print(get_page(url))

    print(get_page(url))
