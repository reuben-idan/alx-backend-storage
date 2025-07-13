#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data using Redis.
"""
import redis
import uuid
from typing import Union

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