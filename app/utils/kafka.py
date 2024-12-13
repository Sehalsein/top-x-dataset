import logging
from confluent_kafka import (
    Producer as KafkaProducer,
    Consumer as KafkaConsumer,
    KafkaError,
)
from confluent_kafka.admin import AdminClient, NewTopic
from typing import List, Callable, Optional
from ..config import get_settings

settings = get_settings()


def create_topic(topic: str, partitions: int = 10):
    """Create a new topic"""
    admin_client = AdminClient({"bootstrap.servers": settings.kafka_bootstrap_server})

    topic_metadata = admin_client.list_topics(timeout=10)

    if topic not in topic_metadata.topics:
        logging.info(f"Creating topic {topic}")
        new_topic = NewTopic(
            topic,
            num_partitions=partitions,
        )
        admin_client.create_topics([new_topic])


class Consumer:

    def __init__(
        self,
        topics: List[str],
        on_message: Callable[[str], None],
        on_error: Optional[Callable[[KafkaError], None]] = None,
    ):
        # Create topics if they don't exist
        for topic in topics:
            create_topic(topic)

        self.consumer = KafkaConsumer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_server,
                "group.id": "basic-consumer",
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe(topics)
        self.on_message = on_message
        self.on_error = on_error

    def consume(self):
        """Consume kafka messages by topic"""
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                error_msg = msg.error()
                if self.on_error:
                    self.on_error(error_msg)
                else:
                    logging.error(f"Consumer error: {error_msg}")
                continue

            self.on_message(msg.value().decode("utf-8"))

    def close(self):
        """Close the consumer"""
        self.consumer.close()


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            {"bootstrap.servers": settings.kafka_bootstrap_server}
        )

    def publish(self, topic: str, data: str):
        """Push messages to a topic"""
        self.producer.produce(topic, data.encode("utf-8"))

    def flush(self):
        self.producer.flush()
