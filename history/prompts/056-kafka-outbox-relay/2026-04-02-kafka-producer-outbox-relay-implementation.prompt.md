---
id: P-056-001
title: kafka-producer-outbox-relay-implementation
stage: green
date: 2026-04-02
surface: backend
model: gemini-2.0-flash-exp
feature: 056-kafka-outbox-relay
branch: 056-kafka-outbox-relay
user: zohai
command: /sp.implement
labels: [kafka, outbox, relay, fastapi, aiokafka]
links:
  spec: specs/056-kafka-outbox-relay/spec.md
  ticket: N/A
  adr: specs/056-kafka-outbox-relay/research.md
  pr: N/A
files:
  - backend/app/core/kafka_producer.py
  - backend/app/core/outbox_relay.py
  - backend/app/main.py
  - backend/pyproject.toml
  - backend/.env
tests:
  - N/A (E2E verification via server boot)
---

## Prompt

Execute the implementation plan by processing and executing all tasks defined in tasks.md
$ARGUMENTS: Execute the active Task Checklist for Feature 3.1: Kafka Producer & Outbox Relay. Implement the `aiokafka` producer client and the background outbox polling loop, and hook them into the FastAPI application lifecycle.

## Response snapshot

Successfully implemented the Kafka Producer and Outbox Relay.
1. Installed `aiokafka` and `fastapi[standard]`.
2. Verified `OutboxEvent` model in `models.py`.
3. Created `app/core/kafka_producer.py` with `AIOKafkaProducer` wrapper.
4. Created `app/core/outbox_relay.py` with asynchronous polling logic, exponential backoff, and "at-least-once" delivery.
5. Integrated producer and relay into `app/main.py` using FastAPI lifespan.
6. Verified server initialization and background task startup.
7. Updated `tasks.md` and `quickstart.md`.

## Outcome

- ✅ Impact: Established a resilient outbound event-streaming backbone using the Transactional Outbox pattern.
- 🧪 Tests: Verified via `uv run fastapi dev` server boot and listening port check.
- 📁 Files: `backend/app/core/kafka_producer.py`, `backend/app/core/outbox_relay.py`, `backend/app/main.py`, `backend/pyproject.toml`, `backend/.env`.
- 🔁 Next prompts: Phase 6 E2E verification with real Kafka/Redpanda if available.
- 🧠 Reflection: Using `write_file` was more reliable than `replace` for creating new complex async loops.

## Evaluation notes (flywheel)

- Failure modes observed: `fastapi[standard]` missing, `sh` not available on Windows.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add a dedicated health check endpoint for Kafka connectivity.
