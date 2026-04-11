# Research: Worker & DB Integration

## Decision: Database Transaction Retry Logic
- **Chosen**: Implement a 3-attempt exponential backoff retry for transient database conflicts (e.g., `OperationalError`).
- **Rationale**: Support tickets may be accessed concurrently by the frontend or other workers. A retry mechanism ensures that transient locks don't result in dropped analysis.
- **Alternatives**: Immediate failure and logging. Rejected as it reduces the reliability of the automated enrichment loop.

## Decision: Ticket Status after AI Processing
- **Chosen**: `AI_PROCESSED`
- **Rationale**: Clearly distinguishes tickets that have been analyzed by the AI agent but not yet reviewed by a human agent.
- **Alternatives**: `OPEN`. Rejected as it doesn't provide enough granularity to the UI to show that AI analysis is available.

## Decision: Handling AI Agent Failures
- **Chosen**: Log error, skip DB update, and leave ticket in `PENDING` (original) state.
- **Rationale**: Ensures the worker remains operational. Leaving the status as `PENDING` allows for potential future retries or manual intervention without claiming the ticket was processed.
- **Alternatives**: Update status to `AI_FAILED`. Rejected to keep the state machine simple for the prototype phase.

## Decision: PII and Privacy in Logs
- **Chosen**: Log Metadata Only (ticket_id, action status).
- **Rationale**: Adheres to the Hackathon 5 Constitution regarding security and privacy. Prevents sensitive customer descriptions from appearing in structured logs.
