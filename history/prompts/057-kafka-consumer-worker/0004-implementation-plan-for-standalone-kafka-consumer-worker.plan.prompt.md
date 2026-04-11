---
id: "0004"
title: "Implementation Plan for Standalone Kafka Consumer Worker"
stage: "plan"
date: "2026-04-04"
surface: "agent"
model: "gemini-2.0-pro-exp"
feature: "057-kafka-consumer-worker"
branch: "057-kafka-consumer-worker"
user: "zohai"
command: "/sp.plan"
labels: ["kafka", "consumer", "worker", "aiokafka", "implementation-plan"]
links:
  spec: "specs/057-kafka-consumer-worker/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/057-kafka-consumer-worker/plan.md"
  - "specs/057-kafka-consumer-worker/research.md"
  - "specs/057-kafka-consumer-worker/data-model.md"
  - "specs/057-kafka-consumer-worker/quickstart.md"
  - "specs/057-kafka-consumer-worker/contracts/support-ticket-event.schema.json"
tests:
  - "n/a (planning phase)"
---

# Prompt

[OBJECTIVE]
Generate a strict Technical Implementation Plan for "Feature 3.2: Standalone Kafka Consumer Worker", based entirely on the active specification. This plan must outline the architecture for a highly reliable, standalone asynchronous Python script that consumes messages from Redpanda.

[INPUT CONTEXT]
Review the current active Specification document for Feature 3.2.
**CRITICAL CONTEXT:** The FastAPI app is already successfully producing messages to the `support.tickets.new` topic. This worker must be entirely decoupled from the FastAPI application and designed to run as its own isolated process (simulating a separate Kubernetes Pod).

[TECHNICAL ARCHITECTURE & DEPENDENCIES]
- Environment: Backend only (`/backend` directory).
- Target Libraries: `aiokafka`, `asyncio`, standard Python `logging`, and `signal`.
- Execution: Direct script execution (`python -m app.workers.main_worker`).

[REQUIRED OUTPUT STRUCTURE]
Your plan must include the following sections:

1. **File Tree Target:**
   Identify the exact file to be created. 
   *(e.g., Create `backend/app/workers/__init__.py` and `backend/app/workers/main_worker.py`).*

2. **Step-by-Step Implementation Logic:**
   Break down the architecture of the script into sequential phases:
   - **Phase A: Configuration & Logging:** Plan the setup of standard Python logging and retrieval of `KAFKA_BROKER_URL` and the target topic from environment variables.
   - **Phase B: Consumer Initialization:** Plan the setup of the `AIOKafkaConsumer`, specifically noting the `group_id` (e.g., `fte-ai-worker-group`) and `value_deserializer` (for JSON parsing).
   - **Phase C: The Polling Loop:** Plan the `async for message in consumer:` loop. Describe the logic: extract the payload, log the Ticket ID and content, and continue. 
   - **Phase D: Signal Handling & Graceful Shutdown:** Plan the critical OS signal handling. Describe how `asyncio.get_running_loop().add_signal_handler()` will be used to catch `SIGINT` and `SIGTERM`, safely break the consumer loop, and call `consumer.stop()` to avoid rebalancing penalties.

3. **Validation Strategy:**
   Define the verification steps. *(e.g., Open a new terminal, run the worker script, submit a form on the Next.js frontend, and observe the worker terminal instantly logging the received Kafka message).*

[CONSTRAINTS & RULES]
- **No FastAPI Coupling:** Explicitly state that this script will NOT import anything from `fastapi` or interact with `main.py`.
- **No AI Logic:** State clearly that OpenAI/LangChain integration is out of scope for this phase.
- **No Code Generation:** This is a planning document only. Output structural outlines and logical flows, but do not write the functional Python code.

# Response

I have generated the strict Technical Implementation Plan for the **Standalone Kafka Consumer Worker**. 

The plan includes:
1.  **File Tree Target**: Creating `backend/app/workers/__init__.py` and `backend/app/workers/main_worker.py`.
2.  **Implementation Phases**: Detailed plans for Configuration, Consumer Initialization, Polling Loop, and Graceful Shutdown.
3.  **Research & Design artifacts**: Created `research.md`, `data-model.md`, `quickstart.md`, and a JSON contract for the support ticket event.
4.  **Agent Context Update**: Updated `GEMINI.md` to reflect the new technology stack.
5.  **Validation Strategy**: Detailed steps to verify the worker by submitting a form on the frontend and observing the logs.

The plan ensures complete decoupling from FastAPI and does not include any AI logic in this phase.
