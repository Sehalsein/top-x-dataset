from typing import List, Tuple
import logging

from app.lib.kafka import consume as kafka_consume, create_topic as kafka_create_topic
from app.lib.redis import client as redis
from app.constants import KafkaTopic, RedisKey

items: List[str] = []

logging.basicConfig(level=logging.DEBUG)


def consumer(message: str):
    """Process incoming messages"""
    try:
        logging.debug(f"Processing message: {message}")
        id, value = parse_item(message)
        update_store(id, value)
    except ValueError as ve:
        logging.error(f"Failed to parse message: {ve}")
    except Exception as e:
        logging.error(f"Something went wrong while processing message {e}")


def parse_item(item: str) -> Tuple[str, int]:
    try:
        id, value = item.strip().split("_")
        return id, int(value)
    except ValueError:
        raise ValueError(f"Invalid item format: {item}")


def update_store(key: str, score: int) -> None:
    """Update Redis sorted sets with new value"""
    try:
        redis.zadd(RedisKey.DATASET.value, {key: score})
    except Exception as e:
        logging.error(f"Failed to update Redis store: {e}")
        raise


if __name__ == "__main__":
    kafka_create_topic(KafkaTopic.DATASET.value)
    logging.info(f"Starting consumer for topic:{KafkaTopic.DATASET.value}...")
    kafka_consume(topics=[KafkaTopic.DATASET.value], on_message=consumer)
