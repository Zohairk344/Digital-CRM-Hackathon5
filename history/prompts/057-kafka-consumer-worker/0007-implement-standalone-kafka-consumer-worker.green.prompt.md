---
id: "0007"
title: "Implement Standalone Kafka Consumer Worker"
stage: "green"
date: "2026-04-04"
surface: "agent"
model: "gemini-2.0-pro-exp"
feature: "057-kafka-consumer-worker"
branch: "057-kafka-consumer-worker"
user: "zohai"
command: "/sp.implement"
labels: ["kafka", "consumer", "worker", "aiokafka", "implementation"]
links:
  spec: "specs/057-kafka-consumer-worker/spec.md"
  plan: "specs/057-kafka-consumer-worker/plan.md"
  tasks: "specs/057-kafka-consumer-worker/tasks.md"
files:
  - "backend/app/workers/__init__.py"
  - "backend/app/workers/main_worker.py"
  - "backend/tests/workers/__init__.py"
  - "backend/tests/workers/test_main_worker.py"
  - "specs/057-kafka-consumer-worker/quickstart.md"
  - "GEMINI.md"
tests:
  - "backend/tests/workers/test_main_worker.py"
---

# Prompt

Execute the active Task Checklist for Feature 3.2: Standalone Kafka Consumer Worker. Implement the isolated `aiokafka` consumer loop, strictly incorporating proper signal handling for graceful shutdowns and robust reconnection logic.

# Response

I have successfully implemented the **Standalone Kafka Consumer Worker**.

### Key Deliverables:
1.  **Worker Script**: Created `backend/app/workers/main_worker.py` which initializes an `AIOKafkaConsumer` with robust reconnection settings (`retry_backoff_ms=500`).
2.  **Graceful Shutdown**: Integrated `SIGINT` and `SIGTERM` handling to break the processing loop and ensure `await consumer.stop()` is called before exit.
3.  **Structured Logging**: Configured `python-json-logger` to output all worker activity in a machine-readable JSON format.
4.  **Testing**: Implemented and verified integration tests in `backend/tests/workers/test_main_worker.py` covering message processing and signal-triggered shutdown.
5.  **Documentation**: Updated `quickstart.md` with execution instructions and `GEMINI.md` with the new worker role.

### How to Run:
1.  Navigate to the backend directory: `cd backend`
2.  Start the worker: `uv run python -m app.workers.main_worker`
