# Research: Standalone Kafka Consumer Worker

This document records the research and technical decisions for the Kafka Consumer Worker.

## Decisions

### 1. Kafka Consumer Configuration
- **Decision**: Use `aiokafka.AIOKafkaConsumer` with `enable_auto_commit=True` and `auto_offset_reset='earliest'`.
- **Rationale**: `aiokafka` is the project standard for async Kafka operations. Auto-commit is sufficient for this logging-only phase. 'earliest' ensures we don't miss historical data if the worker starts late.
- **Alternatives considered**: Manual commit (requires more state management, deferred to future data-persistence phases).

### 2. Graceful Shutdown Implementation
- **Decision**: Use `asyncio.get_running_loop().add_signal_handler()` for `SIGINT` and `SIGTERM`.
- **Rationale**: This is the standard pattern for handling OS signals in an `asyncio` event loop. It allows us to set an `Event` to break the infinite processing loop and call `consumer.stop()`.
- **Alternatives considered**: `signal.signal` (more complex to integrate with `asyncio`).

### 3. Structured Logging
- **Decision**: Use `python-json-logger` to output logs as JSON strings.
- **Rationale**: Meets the requirement for structured JSON format (SC-006/FR-006). Enables easy parsing by log aggregators (ELK, Datadog) without manual parsing.
- **Alternatives considered**: Standard `logging.info` (too unstructured for production-grade worker).

### 4. Standalone Execution
- **Decision**: The worker will be initialized in a `main()` function and run via `python -m app.workers.main_worker`.
- **Rationale**: Decouples the worker lifecycle from FastAPI/Uvicorn. Consistent with Docker/K8s sidecar or standalone pod patterns.

## External Documentation
- [AIOKafka Documentation](https://aiokafka.readthedocs.io/)
- [Asyncio Signal Handling](https://docs.python.org/3/library/asyncio-eventloop.html#unix-signals)
- [Twelve-Factor App: Logs](https://12factor.net/logs)
