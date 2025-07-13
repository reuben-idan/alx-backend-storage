#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data using Redis.
"""
import redis
import uuid
from typing import Union, Callable

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

    def get(self, key: str, fn: 'Callable[[bytes], Union[str, bytes, int, float]]' = None) -> Union[str, bytes, int, float, None]:
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

    def get_str(self, key: str) -> str:
        """
        Retrieve a UTF-8 string from Redis by key.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The retrieved string, or None if the key does not exist.
        """
        data = self.get(key, fn=lambda d: d.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis by key.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The retrieved integer, or None if the key does not exist.
        """
        data = self.get(key, fn=int)
        return data 