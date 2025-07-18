#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data using Redis.
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called using Redis INCR.
    Uses the method's __qualname__ as the key.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function in Redis lists.
    Uses the method's __qualname__ with ':inputs' and ':outputs' suffixes as keys.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Shows the number of calls, inputs, and outputs using Redis lists.
    """
    self = method.__self__
    qualname = method.__qualname__
    inputs_key = f"{qualname}:inputs"
    outputs_key = f"{qualname}:outputs"
    calls = self._redis.get(qualname)
    calls_count = int(calls) if calls else 0
    print(f"{qualname} was called {calls_count} times:")
    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)
    for input_args, output in zip(inputs, outputs):
        print(f"{qualname}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")

class Cache:
    """
    Cache class for storing and retrieving data in Redis.
    """
    def __init__(self) -> None:
        """
        Initialize the Cache instance and flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to store (str, bytes, int, or float).

        Returns:
            The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, bytes, int, float]]] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis by key and optionally apply a conversion function.

        Args:
            key: The key to retrieve from Redis.
            fn: Optional callable to convert the data back to the desired format.

        Returns:
            The retrieved data, possibly converted, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 string from Redis by key.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The retrieved string, or None if the key does not exist.
        """
        data = self.get(key, fn=lambda d: d.decode('utf-8'))
        if isinstance(data, str):
            return data
        return None

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis by key.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The retrieved integer, or None if the key does not exist.
        """
        data = self.get(key, fn=int)
        if isinstance(data, int):
            return data
        return None 