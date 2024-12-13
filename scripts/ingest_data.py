import argparse
import uuid
import random
from typing import List
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)


def generate_value():
    if random.random() < 0.1:  # 10% chance of duplicate
        return random.choice([10, 100, 1000, 10000])

    return random.randint(1, 1000000)


def generate_test_data(count: int):
    data: List[str] = []
    for _ in range(count):
        data.append(f"{uuid.uuid4()}_{generate_value()}")
    return data


async def send_to_api(session: aiohttp.ClientSession, url: str, data: List[str]):
    async with session.post(url, json={"items": data}) as response:
        if response.status != 200:
            logging.error(
                f"Error sending chunk: {response.status}, {await response.text()}"
            )
        else:
            logging.info(f"Chunk sent successfully with status: {response.status}")


async def send_test_data(data: List[str], chunk: int):
    url = "http://localhost:8000/dataset"
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, len(data), chunk):
            logging.debug(f"Preparing chunk {i} for API...")
            chunk_data = data[i : i + chunk]
            tasks.append(send_to_api(session, url, chunk_data))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate test data for the data ingestion pipeline"
    )
    parser.add_argument(
        "--size", type=int, default=1000000, help="Number of records to generate"
    )
    parser.add_argument("--chunk", type=int, default=1000, help="Chunk size for api")

    args = parser.parse_args()

    logging.info(f"Generating {args.size} records...")
    records = generate_test_data(args.size)

    logging.info(f"Sending data in chunks of {args.chunk}...")
    asyncio.run(send_test_data(records, args.chunk))
