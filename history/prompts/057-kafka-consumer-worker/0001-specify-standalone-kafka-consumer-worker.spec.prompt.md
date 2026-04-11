---
id: "0001"
title: "Specify Standalone Kafka Consumer Worker"
stage: "spec"
date: "2026-04-04"
surface: "agent"
model: "gemini-2.0-pro-exp"
feature: "057-kafka-consumer-worker"
branch: "057-kafka-consumer-worker"
user: "zohai"
command: "/sp.specify"
labels: ["kafka", "consumer", "worker", "aiokafka", "specification"]
links:
  spec: "specs/057-kafka-consumer-worker/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/057-kafka-consumer-worker/spec.md"
  - "specs/057-kafka-consumer-worker/checklists/requirements.md"
tests:
  - "n/a (specification phase)"
---

# Prompt

[CONTEXT] Build "Feature 3.2: Standalone Kafka Consumer Worker". The goal is to establish the event-consuming side of the architecture. The FastAPI Producer (Feature 3.1) is now successfully publishing webhook events to the `support.tickets.new` topic in Redpanda. We need a standalone Python script that will act as a separate worker service to consume and log these messages. [TECH STACK & DEPENDENCIES] - Environment: Backend only (`/backend` directory). - Language: Python 3.12+ - Kafka Client: `aiokafka` (to maintain async consistency with the producer) and `asyncio`. - Package Manager: `uv`. [REQUIREMENTS: THE CONSUMER WORKER] 1. **Worker Entrypoint (`app/workers/main_worker.py`):** - Create a standalone Python script that initializes an `AIOKafkaConsumer`. - Connect to Redpanda using the `KAFKA_BROKER_URL` from the environment variables. - Subscribe to the `support.tickets.new` topic. - Configure the consumer with a specific `group_id` (e.g., `fte-ai-worker-group`) to enable offset tracking. 2. **The Processing Loop:** - Implement an infinite asynchronous `for` loop to poll for new messages. - For now, the processing logic should simply deserialize the JSON payload and use standard Python `logging` to print the receipt of the Ticket ID and its contents to the terminal. (AI processing will be added in a future feature). 3. **Graceful Shutdown & Signal Handling:** - The worker MUST handle OS signals (`SIGINT`, `SIGTERM`) safely. - Upon receiving a shutdown signal, it must stop the consumer loop, commit the final offsets, and close the Kafka connection cleanly to avoid consumer group rebalancing penalties. [CONSTRAINTS & BOUNDARIES] - **No API Coupling:** This script must be completely independent of FastAPI. It will not be run via `uvicorn`. It will be executed directly via `python -m app.workers.main_worker`. - **No AI Logic Yet:** Do not import or implement any OpenAI/LangChain logic in this phase. The goal is strictly to establish reliable plumbing and verify message receipt.

# Response

I have initialized the feature branch `057-kafka-consumer-worker` and created the specification at `specs/057-kafka-consumer-worker/spec.md`.

## Key Questions for Finalization:

1. **Error Handling for Malformed Payloads**: How should the system handle messages that are not valid JSON?
   - Option A: Log and Skip (Simple)
   - Option B: Dead-Letter Queue (Robust, requires separate topic)

2. **Offset Reset Strategy**: Where should a new consumer start reading if no offsets are stored?
   - Option A: 'earliest' (No data missed)
   - Option B: 'latest' (Only new data)

I have also created a quality checklist at `specs/057-kafka-consumer-worker/checklists/requirements.md` and initialized the project structure for this feature.
