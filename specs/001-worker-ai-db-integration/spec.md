# Feature Specification: Worker & DB Integration

**Feature Branch**: `001-worker-ai-db-integration`  
**Created**: 2026-04-05  
**Status**: Draft  
**Input**: User description: "[CONTEXT] Build 'Feature 4.2: Worker & DB Integration'. We have a working standalone Kafka worker (app/workers/main_worker.py) and an isolated Gemini AI Agent (app/ai/agent.py). We now need to integrate the AI agent into the Kafka worker's processing loop and update the database with the results. [TECH STACK & DEPENDENCIES] - Environment: Backend only (/backend directory). - Existing Components: app.workers.main_worker, app.ai.agent.process_ticket, app.core.database.async_session_maker, app.models.ticket.Ticket. [REQUIREMENTS: THE INTEGRATION LOGIC] 1. Worker Update (main_worker.py): - Import the process_ticket function from app.ai.agent. - Inside the Kafka consumer async for msg in consumer: loop, extract the ticket payload from the message. - Pass the payload to await process_ticket(payload). 2. Database Update (Closing the Loop): - After receiving the TicketAnalysis (Pydantic object) from the AI, open an async database session using the existing async_session_maker (or dependency). - Fetch the corresponding Ticket record from the database using the ticket_id from the Kafka payload. - Update the ticket with the AI's data: - Save the suggested_response. - Save the category. - Update the ticket status to something like AI_PROCESSED or OPEN. - Commit the transaction. 3. Resilience & Error Handling: - Wrap the AI processing and Database update in a try/except block. - If the AI fails (e.g., API timeout) or the DB update fails, log the error but do not crash the worker loop. The worker must survive to process the next message. [CONSTRAINTS & RULES] - Do not modify the frontend or the FastAPI web endpoints. - Ensure the database connection is cleanly opened and closed within the processing loop to prevent connection leaks."

## Clarifications

### Session 2026-04-05
- Q: Which status should be applied to the ticket after successful AI enrichment to indicate it is ready for human review? → A: `AI_PROCESSED`
- Q: If the AI processing specifically fails (e.g., timeout), but the database is accessible, should we update the ticket status in the DB to reflect this failure, or simply leave it in its original state (e.g., `PENDING`)? → A: Leave as `PENDING`
- Q: If a database lock prevents an update, should the system immediately log it and move on (discarding the analysis), or should we implement a basic retry mechanism (e.g., up to 3 attempts) for transient DB conflicts? → A: Retry 3 times
- Q: For successful processing, what level of logging is required? → A: Metadata Only (`ticket_id` and action status)
- Q: If a Kafka message is received that is improperly formatted or missing the `ticket_id` field entirely, should the worker attempt to DLQ (Dead Letter Queue) the message or simply log a critical error and drop the message? → A: Log and Drop (`ticket_id` unavailable, log raw content)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Ticket Enrichment (Priority: P1)

As a Customer Success Manager, I want incoming tickets to be automatically analyzed and categorized in the database so that my team can immediately see the context and a suggested response when they open a ticket.

**Why this priority**: This is the core "closing the loop" functionality that connects the message stream to the system of record. It enables the actual value of the AI agent to be realized in the UI.

**Independent Test**: Send a test ticket message to the Kafka topic, wait for processing, and verify that the corresponding database record for that ticket ID has been updated with the correct category, suggested response, and a status of `AI_PROCESSED`.

**Acceptance Scenarios**:

1. **Given** a ticket record exists in the DB with status `PENDING`, **When** a Kafka message for that ticket is processed, **Then** the DB record must be updated with AI analysis data and status `AI_PROCESSED`.
2. **Given** a ticket message is received, **When** AI processing completes, **Then** the database transaction must be committed only after all updates are applied.

---

### User Story 2 - Resilient Message Processing (Priority: P2)

As a System Administrator, I want the Kafka worker to remain operational even if the AI service or database encounters intermittent errors so that the system doesn't require manual intervention for every transient failure.

**Why this priority**: Ensures high availability and operational stability. Prevents a single problematic message or external service blip from halting the entire processing pipeline.

**Independent Test**: Simulate an AI service timeout during processing and verify that the error is logged, the worker remains running, and it successfully processes the next message in the queue.

**Acceptance Scenarios**:

1. **Given** the AI service is unreachable, **When** a message is processed, **Then** an error must be logged and the worker must continue to the next Kafka message.
2. **Given** a database connection error occurs for one message, **When** the error is caught, **Then** the worker MUST NOT exit and MUST be ready for the next message.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The worker MUST import and call the `process_ticket` function from the AI agent module for every incoming Kafka message.
- **FR-002**: The system MUST extract the `ticket_id` from the Kafka message payload to identify the target database record.
- **FR-003**: The system MUST use the existing `async_session_maker` to create a scoped database session for each message processing cycle.
- **FR-004**: The system MUST update the `Ticket` record in the database with the `suggested_response` and `category` provided by the AI agent.
- **FR-005**: The system MUST update the ticket status to `AI_PROCESSED` upon successful completion of AI analysis and database persistence.
- **FR-006**: All AI and database operations within the message loop MUST be contained within a `try/except` block to prevent exceptions from crashing the worker.
- **FR-007**: The system MUST ensure that every database session opened for message processing is explicitly and correctly closed, even in the event of an error.
- **FR-008**: The system MUST log successful ticket enrichments using only metadata (e.g., `ticket_id` and action status) to maintain observability without leaking PII.

**Constitution Mandatory Requirements (Inherited from 058):**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries (Handled by AI Agent logic).
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3 (Handled by AI Agent logic).

### Key Entities

- **SupportTicket (DB Model)**: The persisted record representing the customer's request.
- **KafkaMessage**: The transport object containing the ticket payload.
- **TicketAnalysis (Pydantic Model)**: The structured output from the AI agent used to update the DB.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid tickets received via Kafka result in a database update or a logged error entry.
- **SC-002**: Database updates are committed within 500ms of receiving the AI agent's response.
- **SC-003**: The worker process maintains 100% uptime during transient AI service outages (verified by log entries vs process status).
- **SC-004**: System logs capture the specific `ticket_id` and error reason for every failed processing attempt.
- **SC-005**: No increase in database connection count is observed after processing 1,000 messages (zero leaks).

## Edge Cases

- **Missing DB Record**: If a Kafka message arrives for a `ticket_id` that does not exist in the database, the system MUST log a warning and proceed to the next message.
- **Malformed Kafka Message**: If a message is missing the `ticket_id` or is improperly formatted, the system MUST log a critical error with the raw message content (excluding PII) and drop the message.
- **AI Agent Timeout**: If the AI agent fails to respond within its defined timeout, the system MUST log the timeout error and skip the database update for that specific message.
- **Database Transaction Conflict**: If a database lock prevents an update, the system MUST retry the transaction up to 3 times before logging a critical error and moving to the next message.

## Assumptions

- The `app.core.database.async_session_maker` is already configured and functional.
- The `app.models.ticket.Ticket` model has fields for `category`, `suggested_response`, and `status`.
- The Kafka message payload contains a JSON object with at least a `ticket_id` field.
- The `process_ticket` function returns a Pydantic object compatible with the `TicketAnalysis` schema.
- Logging is already configured in the backend environment.
