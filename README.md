# Top X Processor

## Requirements

- Python 3.9 >
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
   make dev
   ```

3. **Start Kafka consumers**:
   ```bash
   make consumer
   ```
   You can start multiple consumers, and the stream will be evenly distributed among all active consumers.

## Performance Optimizations

- **Stream Processing**: Kafka enables parallel processing of data
- **Redis Sorted Sets**: Efficient maintenance of top X values
