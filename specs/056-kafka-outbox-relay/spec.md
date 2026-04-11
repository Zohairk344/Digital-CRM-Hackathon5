# Feature Specification: Kafka Producer & Outbox Relay (Outbound Event Streaming)

**Feature Branch**: `056-kafka-outbox-relay`
**Created**: April 2, 2026
**Status**: Draft
**Input**: User description: "[CONTEXT] Build 'Feature 3.1: Kafka Producer & Outbox Relay'. The goal is to establish the outbound event-streaming backbone of the FastAPI application. We previously implemented the 'Transactional Outbox Pattern' where webhook submissions are securely saved to an `OutboxEvent` database table. Now, we need a Kafka Producer to read those pending events and publish them to a Redpanda (Kafka) broker. [TECH STACK & DEPENDENCIES] - Environment: Backend only (/backend directory). - Language/Framework: Python 3.12+, FastAPI. - Kafka Client: aiokafka (Optimal for asynchronous FastAPI execution). - Broker: Redpanda (Running locally on localhost:9092). - Package Manager: uv. [REQUIREMENTS: THE KAFKA PRODUCER] 1. Client Setup (app/core/kafka_producer.py): - Create a robust Kafka producer class or module using aiokafka. - The producer must connect using the KAFKA_BROKER_URL from the .env file (defaulting to localhost:9092). - Implement a start() and stop() method to manage the connection lifecycle safely. 2. FastAPI Lifespan Integration: - Update app/main.py to use a FastAPI lifespan context manager. - The lifespan must initialize and start the Kafka Producer on app startup, and cleanly shut it down on app termination. [REQUIREMENTS: THE OUTBOX RELAY] 1. The Relay Loop (app/core/outbox_relay.py): - Create an asynchronous background task that runs continuously while the FastAPI app is alive. - Logic: Every X seconds (e.g., 5 seconds), the loop must: a. Query the OutboxEvent table for records where processed == False. b. Publish the payload of each event to a Kafka topic named support.tickets.new. c. Upon successful publish, update the OutboxEvent record to processed = True. 2. Database Safety: - Use the existing database session maker to safely interact with the database without blocking the main FastAPI event loop. [CONSTRAINTS & BOUNDARIES] - Producer Only: Do NOT implement the Kafka Consumer (Worker) in this specification. This feature is strictly for getting data out of FastAPI and into Kafka. - Graceful Failure: If Redpanda is down, the producer/relay must log the error and retry gracefully in the next loop iteration without crashing the entire FastAPI application."

## Clarifications

### Session 2026-04-02
- Q: How should the relay handle persistent publish failures for a specific event? → A: Retry with backoff; fail/skip after 3 attempts
- Q: What should be the maximum batch size for each polling iteration? → A: 50 events per batch (Balanced)
- Q: What are the required delivery semantics for the producer? → A: At-least-once (Safe, potential duplicates)
- Q: What is the required order for publishing events? → A: Sequential by creation time (FIFO)
- Q: How should publish failures and poison messages be tracked/logged for observability? → A: Log to standard application logs

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Event Streaming (Priority: P1)

As a system, I want to automatically stream new webhook submissions from the database to a message broker so that downstream systems can process them in real-time.

**Why this priority**: This is the core functionality required to establish the outbound event-streaming backbone.

**Independent Test**: Can be tested by manually inserting a record into the `OutboxEvent` table and verifying that it appears in the Kafka topic and is subsequently marked as processed in the database.

**Acceptance Scenarios**:

1. **Given** a new record exists in the `OutboxEvent` table with `processed = False`, **When** the outbox relay task runs, **Then** the event payload is published to the `support.tickets.new` topic and the record is updated to `processed = True`.
2. **Given** multiple unprocessed records exist, **When** the relay task runs, **Then** up to 50 pending events are published in sequence (ordered by creation time) and each is marked as processed upon success.

---

### User Story 2 - Resilient Message Delivery (Priority: P2)

As a system, I want to handle temporary message broker outages gracefully so that no event data is lost and streaming resumes automatically once the broker is back online.

**Why this priority**: Ensures system reliability and data integrity during infrastructure instability.

**Independent Test**: Can be tested by stopping the Redpanda broker, adding an outbox event, verifying the relay logs the failure but keeps running, and then starting Redpanda and verifying the event is eventually delivered.

**Acceptance Scenarios**:

1. **Given** the message broker is unavailable, **When** the relay attempt occurs, **Then** the failure is logged and the event remains marked as `processed = False` in the database.
2. **Given** a previously failed delivery, **When** the broker becomes available and the relay runs again, **Then** the event is successfully published and marked as `processed = True`.

---

### User Story 3 - Clean System Lifecycle (Priority: P3)

As a system administrator, I want the event producer to start and stop cleanly with the application so that connections are managed safely and no resources are leaked.

**Why this priority**: Important for operational stability and clean deployments.

**Independent Test**: Can be tested by starting the application and checking logs for successful connection, then stopping the application and verifying clean shutdown of the producer.

**Acceptance Scenarios**:

1. **Given** the application is starting up, **When** the initialization phase completes, **Then** the Kafka connection is established.
2. **Given** the application is shutting down, **When** the termination signal is received, **Then** the Kafka connection is closed gracefully before the process exits.

---

### Edge Cases

- **Broker Connection Timeout**: How does the system handle a slow broker response during the initial connection or a publish event?
- **Concurrent Access**: How does the system handle multiple application instances (if any) polling the same outbox table to avoid duplicate publishing? (Note: Assuming single instance for now based on context).
- **Empty Outbox**: How does the system behave when there are no events to process for an extended period?
- **Poison Messages**: System MUST handle events that consistently fail to publish by moving them to a failed state (e.g., `processed = False`, `retry_count >= 3`) and logging the specific failure reason to standard application logs to prevent blocking the entire relay loop.
- **Duplicate Delivery**: As the system provides "at-least-once" delivery semantics, consumers MUST be prepared to handle duplicate messages.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST establish a connection to the configured Kafka broker upon application startup.
- **FR-002**: System MUST implement a continuous background task that polls the `OutboxEvent` table every 5 seconds.
- **FR-003**: System MUST identify up to 50 records in the `OutboxEvent` table where the `processed` flag is set to `False` per iteration, ordered by creation time (FIFO).
- **FR-004**: System MUST publish the payload of identified events to the `support.tickets.new` topic using "at-least-once" delivery semantics.
- **FR-005**: System MUST update the `processed` flag to `True` for an event only AFTER receiving a successful acknowledgment from the message broker.
- **FR-006**: System MUST ensure that database interactions during the relay loop do not block the main application's responsiveness.
- **FR-007**: System MUST log errors if the broker is unavailable and retry the operation in the next scheduled loop.
- **FR-008**: System MUST gracefully close the broker connection upon application shutdown.
- **FR-009**: System MUST implement an exponential backoff retry mechanism for events that fail to publish.
- **FR-010**: System MUST mark an event as "failed" or skip it after 3 unsuccessful attempts and log the event ID and failure reason to standard application logs.

**Constitution Mandatory Requirements:**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries.
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3.
- **FR-C3**: WhatsApp responses MUST be < 300 characters.
- **FR-C4**: All state MUST be persisted in PostgreSQL.
- **FR-C5**: All events MUST be processed through Kafka/Redpanda.

### Key Entities *(include if feature involves data)*

- **OutboxEvent**: Represents an event waiting to be streamed. Key attributes: `id`, `payload` (the message content), `processed` (boolean status), `retry_count` (integer for failure tracking), and `created_at` (timestamp for ordering).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New events are published to the broker within 10 seconds of being saved to the outbox (assuming 5s poll interval).
- **SC-002**: 100% delivery rate for valid events saved to the outbox, provided the broker eventually recovers from any outages.
- **SC-003**: Zero duplicate marks (processed = True) for events that failed to publish to the broker.
- **SC-004**: Application startup and shutdown times are not negatively impacted by more than 2 seconds by the producer connection lifecycle.

### Assumptions

- **A-001**: The `OutboxEvent` table already exists and is being populated by other parts of the system.
- **A-002**: Only a single instance of the application will be running the relay loop at any given time (no concurrent polling conflict).
- **A-003**: The Kafka broker URL is available in the environment configuration.
