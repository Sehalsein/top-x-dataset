import redis
import logging
from ..config import get_settings


settings = get_settings()


def initialize_redis(host: str, port: int):
    """
    Initializes a Redis connection with retry logic.

    :param host: Redis server hostname.
    :param port: Redis server port.
    :return: A Redis client instance.
    """
    try:
        client = redis.Redis(host=host, port=port, decode_responses=True)
        client.ping()
        return client
    except redis.ConnectionError as e:
        logging.error(f"Redis connection failed: {e}")


try:
    client = initialize_redis(settings.redis_host, settings.redis_port)
except Exception as e:
    logging.error(f"Failed to initialize Redis connection: {e}")
    client = None
