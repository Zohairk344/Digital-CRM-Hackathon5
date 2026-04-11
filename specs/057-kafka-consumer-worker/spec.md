# Feature Specification: Standalone Kafka Consumer Worker

**Feature Branch**: `057-kafka-consumer-worker`  
**Created**: 2026-04-04  
**Status**: Draft  
**Input**: User description: "[CONTEXT] Build \"Feature 3.2: Standalone Kafka Consumer Worker\". The goal is to establish the event-consuming side of the architecture. The FastAPI Producer (Feature 3.1) is now successfully publishing webhook events to the `support.tickets.new` topic in Redpanda. We need a standalone Python script that will act as a separate worker service to consume and log these messages. [TECH STACK & DEPENDENCIES] - Environment: Backend only (`/backend` directory). - Language: Python 3.12+ - Kafka Client: `aiokafka` (to maintain async consistency with the producer) and `asyncio`. - Package Manager: `uv`. [REQUIREMENTS: THE CONSUMER WORKER] 1. **Worker Entrypoint (`app/workers/main_worker.py`):** - Create a standalone Python script that initializes an `AIOKafkaConsumer`. - Connect to Redpanda using the `KAFKA_BROKER_URL` from the environment variables. - Subscribe to the `support.tickets.new` topic. - Configure the consumer with a specific `group_id` (e.g., `fte-ai-worker-group`) to enable offset tracking. 2. **The Processing Loop:** - Implement an infinite asynchronous `for` loop to poll for new messages. - For now, the processing logic should simply deserialize the JSON payload and use standard Python `logging` to print the receipt of the Ticket ID and its contents to the terminal. (AI processing will be added in a future feature). 3. **Graceful Shutdown & Signal Handling:** - The worker MUST handle OS signals (`SIGINT`, `SIGTERM`) safely. - Upon receiving a shutdown signal, it must stop the consumer loop, commit the final offsets, and close the Kafka connection cleanly to avoid consumer group rebalancing penalties. [CONSTRAINTS & BOUNDARIES] - **No API Coupling:** This script must be completely independent of FastAPI. It will not be run via `uvicorn`. It will be executed directly via `python -m app.workers.main_worker`. - **No AI Logic Yet:** Do not import or implement any OpenAI/LangChain logic in this phase. The goal is strictly to establish reliable plumbing and verify message receipt."

## Clarifications

### Session 2026-04-04

- Q: Kafka Connection Security → A: Plaintext (No encryption/authentication)
- Q: Handling of Unknown Fields → A: Log All Fields (Preserve unknown fields in logs)
- Q: Message Processing Retries → A: Immediate Skip (Log error and move to next message)
- Q: Logging Format → A: Structured JSON (Key-value pairs for all logs)
- Q: Configuration of Consumer Group and Topic → A: Configurable (Via `KAFKA_TOPIC` and `KAFKA_GROUP_ID` env vars)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Process Support Tickets (Priority: P1)

As a system worker, I want to automatically consume and log incoming support ticket events from the message broker so that they can be tracked and prepared for future AI processing.

**Why this priority**: This is the core functionality of the feature and establishes the critical event-driven architecture plumbing.

**Independent Test**: Can be tested by running the worker script, producing a test message to the topic, and verifying that the Ticket ID and contents appear in the worker's logs.

**Acceptance Scenarios**:

1. **Given** a message has been published to `support.tickets.new`, **When** the worker is running, **Then** it must log the receipt of the Ticket ID and its JSON payload.
2. **Given** multiple messages are published rapidly, **When** the worker is running, **Then** it must process and log them sequentially in the order received.

---

### User Story 2 - Graceful Termination (Priority: P1)

As a system administrator, I want the worker to shut down cleanly when receiving termination signals (SIGINT, SIGTERM) so that all in-progress message offsets are committed and the consumer group remains stable.

**Why this priority**: Critical for data integrity and operational stability. Prevents rebalancing delays and potential duplicate processing of messages.

**Independent Test**: Can be tested by sending `Ctrl+C` (SIGINT) or a `kill` command (SIGTERM) to the running worker and verifying the logs show a clean shutdown sequence (loop stopped, connection closed).

**Acceptance Scenarios**:

1. **Given** the worker is actively polling messages, **When** a SIGINT signal is received, **Then** the worker must stop the polling loop, commit the last processed offset, and close the connection.
2. **Given** the worker is in a wait state for new messages, **When** a SIGTERM signal is received, **Then** it must exit gracefully without error.

---

### Edge Cases

- **Malformed Payloads**: What happens if a message contains invalid JSON? (Handled via FR-010).
- **Broker Unavailability**: How does the worker handle temporary loss of connection to Redpanda? (Handled via FR-012).
- **Restart from Zero**: Where does the worker start reading if the consumer group is brand new? (Handled via FR-011).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize an asynchronous Kafka consumer using the `KAFKA_BROKER_URL` from the environment via a plaintext connection (no encryption/authentication).
- **FR-002**: System MUST subscribe to the Kafka topic specified by the `KAFKA_TOPIC` environment variable (default: `support.tickets.new`).
- **FR-003**: System MUST use the consumer group ID specified by the `KAFKA_GROUP_ID` environment variable (default: `fte-ai-worker-group`) to enable persistent offset tracking.
- **FR-004**: System MUST implement a non-blocking asynchronous loop that continuously polls for new messages.
- **FR-005**: System MUST deserialize incoming JSON payloads into Python dictionary objects.
- **FR-006**: System MUST log the `Ticket ID` and the full message content (including any additional unknown fields) in structured JSON format to the terminal upon successful receipt.
- **FR-007**: System MUST intercept `SIGINT` and `SIGTERM` signals to initiate a shutdown sequence.
- **FR-008**: System MUST ensure final offsets are committed to the broker before the process exits.
- **FR-009**: System MUST be executable as a standalone module using `python -m app.workers.main_worker`.
- **FR-010**: System MUST handle malformed JSON payloads and internal processing errors by logging the error in structured JSON format and skipping the message (Log and Skip).
- **FR-011**: System MUST start reading from the 'earliest' offset when joining a consumer group for the first time to ensure no historical data is missed.
- **FR-012**: System MUST attempt to reconnect to the broker if the connection is lost during execution.

**Constitution Mandatory Requirements:**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries. (Not applicable in this plumbing phase, but reserved for future AI logic).
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3. (Not applicable in this plumbing phase).
- **FR-C3**: WhatsApp responses MUST be < 300 characters. (Not applicable).
- **FR-C4**: All state MUST be persisted in PostgreSQL. (Offsets are persisted in Kafka, Ticket state in DB will be in future phases).
- **FR-C5**: All events MUST be processed through Kafka/Redpanda. (This feature implements the consumption side of this requirement).

### Key Entities

- **Support Ticket Event**: Represents a new support ticket webhook event. Key attributes include `Ticket ID`, `Subject`, `Description`, and `Metadata`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages successfully published to `support.tickets.new` are accurately logged by the worker within 1 second of receipt.
- **SC-002**: Worker process exits cleanly within 5 seconds of receiving a termination signal.
- **SC-003**: Worker remains completely independent of the FastAPI application runtime (can run without Uvicorn or API dependencies).
- **SC-004**: System supports a message throughput of at least 100 messages per second on standard dev environment hardware.
