# Data Model: Support Ticket Event

This document defines the structure of the message payload consumed from the `support.tickets.new` topic.

## Entity: Support Ticket Event
Represents a new support ticket submitted via the web form.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `ticket_id` | `UUID` | Unique identifier for the ticket. | Yes |
| `subject` | `String` | Short summary of the issue. | Yes |
| `description` | `String` | Detailed description of the user's issue. | Yes |
| `metadata` | `Dict` | Additional context (e.g., user agent, origin). | Yes |
| `status` | `String` | Initial status (e.g., "new"). | Yes |
| `timestamp` | `ISO8601` | When the event was created. | Yes |

## Uniqueness & Constraints
- `ticket_id` must be a valid UUID.
- All required fields must be present in the JSON payload.
- Payload must be valid JSON (UTF-8).

## State Transitions
1. **Source**: Produced by FastAPI Web Support Form.
2. **Action**: Consumed by `main_worker.py`.
3. **Outcome**: Logged to terminal/stdout in structured JSON.
