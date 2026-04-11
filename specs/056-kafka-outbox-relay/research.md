# Research: Kafka Producer & Outbox Relay

## Decision: Kafka Client Selection
- **Choice**: `aiokafka`
- **Rationale**: Optimal for asynchronous FastAPI execution. It allows the producer to connect, send, and stop without blocking the main event loop.
- **Alternatives considered**: `confluent-kafka` (already in `pyproject.toml`). While powerful, `aiokafka` provides a more idiomatic async API for Python's `asyncio` compared to the wrapper-based approach of `confluent-kafka`. Given the low complexity of a producer-only requirement, `aiokafka` is preferred for developer experience in an async context.

## Decision: Polling Strategy
- **Choice**: Continuous loop with `asyncio.sleep(5)`.
- **Rationale**: Simple, effective, and fulfills the requirement for a background task that runs while the app is alive. It prevents overwhelming the database while maintaining a low latency for event streaming.
- **Alternatives considered**: PostgreSQL `LISTEN/NOTIFY`. While lower latency, it adds complexity to the database connection management and is less robust for "guaranteed" processing compared to polling a table with a status flag.

## Decision: Outbox Processing Lifecycle
- **Choice**: "At-least-once" delivery with batching.
- **Rationale**: Ensuring an event is marked as `processed=True` ONLY after successful Kafka acknowledgment ensures no data loss. Batching (50 events) optimizes database and network overhead.
- **Alternatives considered**: Single event processing. Rejected due to inefficiency under high volume.

## Decision: Resilience & Poison Messages
- **Choice**: Retry with exponential backoff (1s initial, 2x factor, 60s max) and a hard limit of 3 attempts. Catch `KafkaConnectionError` and `RequestTimeoutError` for retries.
- **Rationale**: Prevents a single malformed or consistently failing event from blocking the entire outbound stream (Head-of-Line blocking).
- **Alternatives considered**: Infinite retries. Rejected because it blocks all subsequent events if one is permanently unpublishable.

## Decision: Observability
- **Choice**: Standard application logs.
- **Rationale**: Consistent with existing FastAPI logging patterns and easily integrable with container log aggregation.
- **Alternatives considered**: Dedicated failure table. Rejected for MVP to minimize schema complexity, though noted as a future improvement.
