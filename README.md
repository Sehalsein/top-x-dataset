# Top X Processor

## Requirements

- Python 3.9 or greater
- Docker and Docker compose
- Make

## Architecture Overview

- **FastAPI**: Provides REST API endpoints for data ingestion.
- **Kafka**: Handles stream processing of data.
- **Redis**: Store to persist data.

## Setup

1. **Start the required stack using Docker**:

   ```bash
   docker-compose up --build
   ```

2. **Start the FastAPI server**:

   ```bash
   make start
   ```

3. **Start Kafka consumers**:

   ```bash
   make consumer
   ```

   You can start multiple consumers, and the data stream will be evenly distributed among all active consumers.

4. **Generate Test Data**:

   To ingest data:

   ```bash
   make ingest
   ```

   By default, 100K records are ingested. To change the number of records, pass the `--size` argument to the script.

   For example, to ingest 1M records:

   ```bash
   make ingest ARGS="--size=1000000"
   ```

## API Endpoints

### POST - /dataset

Publish dataset items and return processing statistics.

```bash
curl --location 'http://localhost:8000/dataset' \
--header 'Content-Type: application/json' \
--data '{
    "items": [
        "11111111_10",
        "22222222_10",
        "33333333_11",
        "12345678_10001",
        "23456789_10001"
    ]
}'
```

### GET - /dataset

Retrieve dataset items, ordered by value.

#### Query Parameters

- `limit` (integer)

To return the top X records, set the `limit` parameter.

For example, to return the top 10 records:

```bash
curl --location 'http://localhost:8000/dataset?limit=10'
```

### DELETE - /dataset

Clear the dataset from the store.

```bash
curl --location --request DELETE 'http://localhost:8000/dataset'
```

## Performance Optimizations

- **Stream Processing**: Utilize Kafka for parallel data processing.
- **Redis Sorted Sets**: Efficiently manage and maintain top X values.

### Time Complexity

- POST /dataset - O(N) each item is sent to kafka for processing
- GET /dataset - O(log(N) + M) with N being the number of elements in the sorted set and M the number of elements returned.

### Space Complexity

- POST /dataset - O(N) where N is the no of items
- GET /dataset - O(M) where M is the number of elements returned

### Enabling Profiling

To enable profiling, add the following line to your `.env` file:

```plaintext
PROFILING=true
```

For production-level profiling and performance monitoring, tools like [Sentry](https://sentry.io/welcome/) or [New Relic](https://newrelic.com/) are very useful. These tools provide detailed insights and metrics to help analyze and optimize the application's real-world performance.
