# Data Model: Kafka Outbox Relay

## Entity: OutboxEvent (Existing)

The `OutboxEvent` table serves as the persistent buffer for the Transactional Outbox Pattern.

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key (from `IDMixin`) |
| `event_type` | String(100) | Type of event (e.g., `ticket_created`) |
| `payload` | JSONB | Data payload intended for Kafka |
| `status` | String(20) | Current state: `pending`, `processed`, `failed` |
| `retry_count` | Integer | Number of failed publish attempts (NEW attribute to be added/verified) |
| `created_at` | DateTime | Creation timestamp (from `TimestampMixin`) |
| `updated_at` | DateTime | Last update timestamp (from `TimestampMixin`) |

## State Transitions

1. **Pending**: Initial state when a webhook creates the event record.
2. **Processed**: Terminal state after successful Kafka acknowledgment.
3. **Failed**: Terminal state after 3 unsuccessful attempts (with backoff).

## Relationships

- **Logical Connection**: Each `OutboxEvent` payload typically contains the `ticket_id` and associated customer data from the `Ticket` entity, but the table itself is decoupled from core entities to allow for generic event streaming.
