# Implementation Plan: Kafka Producer & Outbox Relay (Outbound Event Streaming)

**Branch**: `056-kafka-outbox-relay` | **Date**: April 2, 2026 | **Spec**: [specs/056-kafka-outbox-relay/spec.md](spec.md)
**Input**: Feature specification for outbound event streaming from PostgreSQL via a Transactional Outbox pattern.

## Summary

Establish a resilient outbound event-streaming backbone for the FastAPI application. This involves implementing a robust Kafka Producer using `aiokafka` and an asynchronous background "Outbox Relay" task that periodically polls the `OutboxEvent` table, publishes pending records to Redpanda (Kafka), and marks them as processed upon success.

## Technical Context

**Language/Version**: Python 3.12+ (uv)
**Primary Dependencies**: FastAPI, aiokafka, SQLAlchemy (Async)
**Storage**: PostgreSQL (Existing `OutboxEvent` table)
**Testing**: Pytest (Async)
**Target Platform**: Dockerized Backend / Redpanda (localhost:9092)
**Project Type**: Backend-only service integration
**Performance Goals**: Events processed within 10s of creation; 5s polling interval; "At-least-once" delivery guarantee.
**Constraints**: Producer-only (No consumer/worker logic); Must not block main FastAPI event loop; Graceful failure if Redpanda is unreachable.
**Scale/Scope**: 50 events per batch; Single polling instance (Assume no concurrent instances).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Role & Autonomy**: Is the architect role fully assumed? (Lead Digital FTE Architect)
- [x] **II. Technical Stack Sovereignty**: Are Python 3.12+, uv, FastAPI, Next.js, and Redpanda used?
- [x] **III. Architectural Standards**: Is the monorepo (/backend, /frontend, /infra) structure followed? Is it event-driven?
- [x] **IV. Business Logic Constraints**: Are the FTE Handbook rules (pricing, sentiment, channel limits) integrated? (Escalation logic handled by event processors downstream).
- [x] **V. Coding Style & Safety**: Are strict types and robust error handling planned?
- [x] **VI. Operational Procedure**: Is the Web Support Form prioritized? Is the plan explained step-by-step?

## Project Structure

### Documentation (this feature)

```text
specs/056-kafka-outbox-relay/
├── plan.md              # This file
├── research.md          # Decision log and Rationale
├── data-model.md        # OutboxEvent entity details
└── quickstart.md        # Setup and verification guide
```

### Source Code Target File Tree

```text
backend/
├── app/
│   ├── core/
│   │   ├── kafka_producer.py    # NEW: AIOKafkaProducer wrapper
│   │   ├── outbox_relay.py      # NEW: Background polling task
│   │   └── config.py            # MODIFIED: Added Kafka settings
│   ├── db/
│   │   └── models.py            # MODIFIED: Add retry_count if missing
│   └── main.py                  # MODIFIED: Lifespan integration
├── .env                         # MODIFIED: KAFKA_BROKER_URL
└── pyproject.toml               # MODIFIED: Add aiokafka dependency
```

## Step-by-Step Implementation Logic

### Phase A: Kafka Producer Client (`kafka_producer.py`)
- Define a class `KafkaProducer` that wraps `AIOKafkaProducer`.
- Implement `start()` and `stop()` methods triggered by FastAPI's `lifespan`.
- Implement `send_message(topic, payload)` with robust error handling (broker connection loss, topic authorization errors, and payload serialization failures).

### Phase B: Outbox Relay Loop (`outbox_relay.py`)
- Implement `run_outbox_relay()` as an `async` function.
- Polling logic:
  1. Acquire a database session using `AsyncSessionLocal`.
  2. Query `OutboxEvent` where `status == "pending"` (limit 50, ordered by `created_at` ASC for FIFO).
  3. For each event:
     - Publish payload to `support.tickets.new` via `KafkaProducer`.
     - On success: Update `status = "processed"`.
     - On failure: Increment `retry_count`. If `retry_count >= 3`, update `status = "failed"`.
  4. `await asyncio.sleep(5)`.
- Ensure exceptions are caught inside the loop to prevent the background task from crashing.

### Phase C: FastAPI Lifespan Integration (`main.py`)
- Define an `@asynccontextmanager` function for the FastAPI `lifespan`.
- Initialize and `start()` the `KafkaProducer` on startup.
- Start the `run_outbox_relay()` background task via `asyncio.create_task()`.
- On shutdown: Cancel the relay task and `stop()` the `KafkaProducer` gracefully.

## Validation Strategy
1. **Dependency Check**: `uv add aiokafka`.
2. **Integration Test**: Manually insert a record into `outbox_event` and verify status changes to `processed`.
3. **Log Audit**: Verify "Published" or "Failure" logs appear in standard output.
4. **Broker Resilience**: Stop Redpanda and verify that the relay retries without crashing the backend.
