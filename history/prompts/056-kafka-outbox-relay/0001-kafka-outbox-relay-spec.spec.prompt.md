---
id: 0001
title: kafka-outbox-relay-spec
stage: spec
date: 2026-04-02
surface: terminal
model: gemini-cli
feature: 056-kafka-outbox-relay
branch: 056-kafka-outbox-relay
user: zohai
command: /sp.specify
labels: [spec, kafka, outbox]
links:
  spec: specs/056-kafka-outbox-relay/spec.md
  ticket: 
  adr: 
  pr: 
files:
  - specs/056-kafka-outbox-relay/spec.md
  - specs/056-kafka-outbox-relay/checklists/requirements.md
tests:
---

## Prompt

[CONTEXT] Build "Feature 3.1: Kafka Producer & Outbox Relay". The goal is to establish the outbound event-streaming backbone of the FastAPI application. We previously implemented the "Transactional Outbox Pattern" where webhook submissions are securely saved to an `OutboxEvent` database table. Now, we need a Kafka Producer to read those pending events and publish them to a Redpanda (Kafka) broker. [TECH STACK & DEPENDENCIES] - Environment: Backend only (`/backend` directory). - Language/Framework: Python 3.12+, FastAPI. - Kafka Client: `aiokafka` (Optimal for asynchronous FastAPI execution). - Broker: Redpanda (Running locally on `localhost:9092`). - Package Manager: `uv`. [REQUIREMENTS: THE KAFKA PRODUCER] 1. **Client Setup (`app/core/kafka_producer.py`):** - Create a robust Kafka producer class or module using `aiokafka`. - The producer must connect using the `KAFKA_BROKER_URL` from the `.env` file (defaulting to `localhost:9092`). - Implement a `start()` and `stop()` method to manage the connection lifecycle safely. 2. **FastAPI Lifespan Integration:** - Update `app/main.py` to use a FastAPI `lifespan` context manager. - The lifespan must initialize and start the Kafka Producer on app startup, and cleanly shut it down on app termination. [REQUIREMENTS: THE OUTBOX RELAY] 1. **The Relay Loop (`app/core/outbox_relay.py`):** - Create an asynchronous background task that runs continuously while the FastAPI app is alive. - **Logic:** Every X seconds (e.g., 5 seconds), the loop must: a. Query the `OutboxEvent` table for records where `processed == False`. b. Publish the payload of each event to a Kafka topic named `support.tickets.new`. c. Upon successful publish, update the `OutboxEvent` record to `processed = True`. 2. **Database Safety:** - Use the existing database session maker to safely interact with the database without blocking the main FastAPI event loop. [CONSTRAINTS & BOUNDARIES] - **Producer Only:** Do NOT implement the Kafka Consumer (Worker) in this specification. This feature is strictly for getting data *out* of FastAPI and into Kafka. - **Graceful Failure:** If Redpanda is down, the producer/relay must log the error and retry gracefully in the next loop iteration without crashing the entire FastAPI application.

## Response snapshot

Created the feature specification for the Kafka Producer & Outbox Relay. The specification (specs/056-kafka-outbox-relay/spec.md) defines the functional requirements for periodic polling of the `OutboxEvent` table, reliable publishing to Kafka, and clean lifecycle management. A quality checklist was created and completed to ensure the specification remains focused on "what" rather than "how".

## Outcome

- ✅ Impact: Established a clear functional baseline for the outbound event streaming feature.
- 🧪 Tests: Defined acceptance scenarios for automated streaming, broker resilience, and lifecycle management.
- 📁 Files: `specs/056-kafka-outbox-relay/spec.md`, `specs/056-kafka-outbox-relay/checklists/requirements.md`
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Successfully translated technical implementation details into high-level functional requirements suitable for business stakeholders while preserving the core logic of the transactional outbox pattern.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
