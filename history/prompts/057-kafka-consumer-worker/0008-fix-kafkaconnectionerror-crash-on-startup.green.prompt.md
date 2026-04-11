---
id: "0008"
title: "Fix KafkaConnectionError crash on startup"
stage: "green"
date: "2026-04-04"
surface: "agent"
model: "gemini-2.0-pro-exp"
feature: "057-kafka-consumer-worker"
branch: "057-kafka-consumer-worker"
user: "zohai"
command: "/sp.implement"
labels: ["kafka", "error-handling", "retry", "main_worker"]
links:
  spec: "specs/057-kafka-consumer-worker/spec.md"
  plan: "specs/057-kafka-consumer-worker/plan.md"
  tasks: "specs/057-kafka-consumer-worker/tasks.md"
files:
  - "backend/app/workers/main_worker.py"
  - "backend/tests/workers/test_main_worker_retry.py"
tests:
  - "backend/tests/workers/test_main_worker.py"
  - "backend/tests/workers/test_main_worker_retry.py"
---

# Prompt

Fix the `KafkaConnectionError` crash on startup in `main_worker.py`.

[EXECUTION PROTOCOL]
1. Change directory to `/backend`.
2. Open `app/workers/main_worker.py`.
3. Locate the `await consumer.start()` call. 
4. Wrap this specific call in an asynchronous `while True` loop with a `try/except` block catching `aiokafka.errors.KafkaConnectionError`.
5. If it fails, log a warning (e.g., "Kafka broker unavailable, retrying in 5 seconds...") and `await asyncio.sleep(5)` before trying again. Break the loop once `start()` succeeds.
6. Do not alter the rest of the consumer message-polling loop or the signal handlers.

# Response

I have fixed the `KafkaConnectionError` crash on startup by wrapping the `consumer.start()` call in a retry loop.

### Changes:
- Modified `backend/app/workers/main_worker.py` to import `KafkaConnectionError`.
- Implemented an asynchronous `while True` loop around `await consumer.start()`.
- Added a `try/except` block to catch `KafkaConnectionError`, log a warning, and sleep for 5 seconds before retrying.
- Created a new test `backend/tests/workers/test_main_worker_retry.py` to verify the retry logic.
- Synchronized the `backend` environment using `uv sync` to ensure all dependencies (like `pgvector` required by conftest) are present.

All tests passed, including existing integration tests and the new retry logic test.
