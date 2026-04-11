# Implementation Plan: Standalone Kafka Consumer Worker

**Branch**: `057-kafka-consumer-worker` | **Date**: 2026-04-04 | **Spec**: [specs/057-kafka-consumer-worker/spec.md]
**Input**: Feature specification from `/specs/057-kafka-consumer-worker/spec.md`

## Summary

The goal is to implement a standalone asynchronous Python worker that consumes support ticket events from a Redpanda/Kafka topic (`support.tickets.new`). The worker will use `aiokafka` for non-blocking I/O, implement structured JSON logging for all received messages, and handle OS signals (`SIGINT`, `SIGTERM`) for a graceful shutdown. This worker is decoupled from the FastAPI producer and designed to run as an independent process.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `aiokafka`, `asyncio`, `python-json-logger` (for structured logging), `pydantic` (for validation)  
**Storage**: N/A (Event-driven consumption, offsets managed by Kafka)  
**Testing**: `pytest`, `pytest-asyncio`  
**Target Platform**: Linux / Docker / Kubernetes  
**Project Type**: Backend (Standalone Worker)  
**Performance Goals**: Support throughput of at least 100 messages per second.  
**Constraints**: <5s graceful shutdown, zero coupling with FastAPI runtime, structured JSON output.  
**Scale/Scope**: Single worker entrypoint in `backend/app/workers/main_worker.py`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Role & Autonomy**: Is the architect role fully assumed? (Lead Digital FTE Architect)
- [x] **II. Technical Stack Sovereignty**: Are Python 3.12+, uv, FastAPI, Next.js, and Redpanda used?
- [x] **III. Architectural Standards**: Is the monorepo structure followed? Is it event-driven?
- [x] **IV. Business Logic Constraints**: Are the FTE Handbook rules integrated? (Reserved for future phases)
- [x] **V. Coding Style & Safety**: Are strict types and robust error handling planned?
- [x] **VI. Operational Procedure**: Is the plan explained step-by-step?

## Project Structure

### Documentation (this feature)

```text
specs/057-kafka-consumer-worker/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Validation checklists
└── spec.md              # Feature specification
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── workers/
│   │   ├── __init__.py
│   │   └── main_worker.py    # Standalone entrypoint
│   └── ...
├── tests/
│   ├── workers/
│   │   └── test_main_worker.py
│   └── ...
└── pyproject.toml
```

**Structure Decision**: Using the existing `backend/` structure but adding a `workers/` package to isolate background processing logic from the API.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
