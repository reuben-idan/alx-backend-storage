# 0x02. Redis basic

This project demonstrates basic usage of Redis in Python, including storing and retrieving data using a custom `Cache` class. The `exercise.py` module provides a class for interacting with a Redis database, with methods for storing data under randomly generated keys.

## Redis Setup Instructions

### On Ubuntu 18.04

```
# Install Redis server
sudo apt-get -y install redis-server

# Install the Python Redis client
pip3 install redis

# Configure Redis to bind only to localhost
sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf

# Start Redis server
sudo service redis-server start
```

### Using Redis in a Docker Container

```
# Pull the latest Redis image
# (Requires Docker to be installed)
docker pull redis:latest

# Run Redis in a container, binding to localhost:6379
docker run -d --name redis-server -p 6379:6379 redis:latest

# To stop the container
docker stop redis-server

# To start the container again
docker start redis-server
```

> **Note:** On Windows, you can use Docker Desktop to run Redis in a container. If you need to run Ubuntu commands natively, consider using WSL (Windows Subsystem for Linux) or a virtual machine.
