from typing import List, Tuple
import logging

from app.utils.kafka import Consumer as KafkaConsumer
from app.utils.redis import client as redis
from app.constants import KafkaTopic, RedisKey

items: List[str] = []

logging.basicConfig(level=logging.DEBUG)


def process_message(message: str):
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
    logging.info(f"Starting consumer for topic:{KafkaTopic.DATASET.value}...")
    kafka_consumer = KafkaConsumer(
        topics=[KafkaTopic.DATASET.value], on_message=process_message
    )
    try:
        kafka_consumer.consume()
    except KeyboardInterrupt:
        logging.info("Shutting down consumer...")
    except Exception as e:
        logging.error(f"Consumer error: {e}")
    finally:
        kafka_consumer.close()
