#!/usr/bin/env python3
"""
This module provides a web caching system with URL access tracking using Redis.
"""
import requests
import redis
import time
from typing import Optional
from functools import wraps

# Initialize Redis connection
redis_client = redis.Redis()

def count_url_access(url: str) -> None:
    """
    Increment the access count for a specific URL in Redis.
    
    Args:
        url: The URL to track access count for.
    """
    key = f"count:{url}"
    redis_client.incr(key)

def cache_with_expiry(url: str, content: str, expiry: int = 10) -> None:
    """
    Cache the content for a URL with expiration time.
    
    Args:
        url: The URL to cache content for.
        content: The HTML content to cache.
        expiry: Expiration time in seconds (default: 10).
    """
    key = f"cache:{url}"
    redis_client.setex(key, expiry, content)

def get_cached_content(url: str) -> Optional[str]:
    """
    Retrieve cached content for a URL if it exists and hasn't expired.
    
    Args:
        url: The URL to get cached content for.
        
    Returns:
        The cached content if available, None otherwise.
    """
    key = f"cache:{url}"
    content = redis_client.get(key)
    if content:
        return content.decode('utf-8')
    return None

def get_page(url: str) -> str:
    """
    Get the HTML content of a URL with caching and access tracking.
    
    This function:
    1. Checks if content is cached and not expired
    2. If cached, returns the cached content
    3. If not cached, fetches from URL, caches with 10-second expiry
    4. Tracks access count for the URL
    
    Args:
        url: The URL to fetch HTML content from.
        
    Returns:
        The HTML content of the URL.
    """
    # Track URL access
    count_url_access(url)
    
    # Check if content is cached
    cached_content = get_cached_content(url)
    if cached_content:
        return cached_content
    
    # Fetch content from URL
    response = requests.get(url)
    content = response.text
    
    # Cache the content with 10-second expiration
    cache_with_expiry(url, content, 10)
    
    return content 