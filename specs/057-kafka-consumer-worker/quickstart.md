# Quickstart: Standalone Kafka Consumer Worker

This guide provides instructions on how to run and verify the worker service.

## Prerequisites
- Redpanda/Kafka broker running locally or via Docker.
- Python 3.12+ and `uv` installed.
- `.env` file with `KAFKA_BROKER_URL` configured.

## 1. Environment Configuration
Ensure your environment has the following variables (defaults are used if missing):
```bash
KAFKA_BROKER_URL=localhost:9092
KAFKA_TOPIC=support.tickets.new
KAFKA_GROUP_ID=fte-ai-worker-group
LOG_LEVEL=INFO
```

## 2. Running the Worker
Run the worker directly from the `backend/` directory using `uv`:
```bash
cd backend
uv run python -m app.workers.main_worker
```

## 3. Verification Steps
1. **Frontend**: Submit a ticket via the Web Support Form.
2. **Backend (API)**: Ensure the API produces the event to the topic.
3. **Worker Terminal**: Observe the output. You should see a structured JSON log entry containing the `ticket_id` and the ticket details.

### Expected Log Output Format
```json
{"asctime": "...", "levelname": "INFO", "name": "root", "message": "Support Ticket Received", "ticket_id": "...", "payload_snippet": "...", "full_payload": {...}}
```

## 4. Graceful Shutdown
To stop the worker, press `Ctrl+C` (SIGINT) or send a `SIGTERM`. The worker will log:
```json
{"message": "Stopping consumer and committing offsets..."}
{"message": "Worker stopped gracefully"}
```

## 5. Running Tests
To run the automated tests for the worker:
```bash
cd backend
uv run pytest tests/workers/test_main_worker.py
```
