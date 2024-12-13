import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .config import get_settings
from .constants import KafkaTopic, RedisKey
from .models import IngestDataRequest
from .utils.redis import client as redis
from .utils.kafka import (
    Producer as KafkaProducer,
    create_topic as kafka_create_topic,
)

kafka_producer = KafkaProducer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_create_topic(KafkaTopic.DATASET.value)
    yield


app = FastAPI(lifespan=lifespan)
settings = get_settings()


@app.get("/")
async def read_root():
    return {
        "version": settings.version,
        "service": settings.app_name,
    }


@app.post("/dataset")
async def post_dataset(data: IngestDataRequest):
    """Publish dataset items and return processing statistics."""
    start_time = time.time()
    records_processed = 0

    try:
        for line in data.items:
            kafka_producer.publish(KafkaTopic.DATASET.value, line)
            records_processed += 1

        kafka_producer.flush()
    except Exception as e:
        logging.error(f"Error while processing dataset: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to process dataset. Please try again later."
        )

    processing_time = time.time() - start_time

    return {"count": records_processed, "time": processing_time}


@app.get("/dataset")
async def get_dataset(limit: int = 0):
    """Retrieve dataset items, ordered by value."""

    try:
        if limit <= 0:
            limit = -1
        else:
            limit = limit - 1

        result = redis.zrevrange(RedisKey.DATASET.value, 0, limit)
        return {"data": list(result)}
    except Exception as e:
        logging.error(f"Error while retrieving dataset: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dataset. Please try again later.",
        )


@app.delete("/dataset")
async def delete_dataset():
    """Clear the dataset"""
    try:
        redis.delete(RedisKey.DATASET.value)
        return {"message": "Dataset cleared"}
    except Exception as e:
        logging.error(f"Error clearing dataset {e}")
        raise HTTPException(
            status_code=500, detail="Failed to clear dataset. Please try again later."
        )
