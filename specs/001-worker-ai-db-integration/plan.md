# Implementation Plan: Worker & DB Integration

**Branch**: `001-worker-ai-db-integration` | **Date**: 2026-04-05 | **Spec**: [specs/001-worker-ai-db-integration/spec.md]

## Summary

Bridge the Kafka message consumer loop with the completed Gemini AI Agent to automatically enrich support tickets with category, sentiment, and suggested responses, persisting the results to the PostgreSQL database.

## Technical Context

**Language/Version**: Python 3.13+  
**Primary Dependencies**: `aiokafka`, `sqlalchemy` (Async), `langchain-google-genai`, `pydantic`  
**Storage**: PostgreSQL  
**Testing**: `pytest`, `pytest-asyncio`  
**Target Platform**: Linux Server (Dockerized)
**Project Type**: Backend (FastAPI + Kafka Worker)  
**Performance Goals**: Processing time under 5 seconds per ticket (LLM target)  
**Constraints**: < 200ms p95 for DB updates, no connection leaks  
**Scale/Scope**: Targeted for Stage 1 prototyping, scalable via Kafka consumer groups

## Constitution Check

- [x] **I. Role & Autonomy**: Assumed architect role for integration.
- [x] **II. Technical Stack Sovereignty**: Using Python 3.12+, uv, SQLAlchemy (Async), and Redpanda/Kafka.
- [x] **III. Architectural Standards**: Monorepo backend separation maintained. Event-driven integration.
- [x] **IV. Business Logic Constraints**: AI Agent core handles sentiment (<0.3) and pricing escalation.
- [x] **V. Coding Style & Safety**: Using strict types (Pydantic models) and async database handling.
- [x] **VI. Operational Procedure**: Integration loop explained step-by-step.

## Project Structure

### Documentation (this feature)

```text
specs/001-worker-ai-db-integration/
├── plan.md              # This file
├── research.md          # Integration and model decisions
├── data-model.md        # Updated Ticket schema
├── quickstart.md        # Execution and verification guide
└── tasks.md             # (Future)
```

### Source Code

```text
backend/
├── app/
│   ├── ai/
│   │   └── agent.py     # Existing AI Logic
│   ├── db/
│   │   ├── models.py    # Ticket model updates
│   │   └── database.py  # Async session factory
│   └── workers/
│       └── main_worker.py # Integration loop modification
└── tests/
    └── workers/
        └── test_integration.py # New end-to-end integration tests
```

## Detailed Plan

### 1. Schema Update (Database)
- **Model Modification**: Update `backend/app/db/models.py` to add `category`, `suggested_response`, and `is_escalated` to the `Ticket` model.
- **Verification**: Run `uv run app/db/init_db.py` to ensure tables are correctly created/updated.

### 2. File Modifications (`main_worker.py`)
- **Imports**: 
  - `from app.ai.agent import AIAgent, SupportTicket`
  - `from app.db.database import AsyncSessionLocal`
  - `from app.db.models import Ticket`
- **Logic Breakdown**:
  - *Initialize*: Create an instance of `AIAgent` before the loop.
  - *Integration Loop*:
    1. **Payload Extraction**: Parse `msg.value` as JSON. Validate `ticket_id`.
    2. **AI Invocation**: 
       - Map Kafka payload to `SupportTicket` Pydantic model.
       - `analysis = await agent.process_ticket(ticket_input)`
    3. **Database Transaction**:
       - Open `AsyncSessionLocal` using `async with`.
       - Fetch `Ticket` by UUID.
       - Update fields: `category`, `suggested_response`, `is_escalated`, and set `status = "AI_PROCESSED"`.
       - `commit()` transaction.
       - Handle 3-attempt retry logic for database conflicts.

### 3. Resilience Strategy
- Wrap the entire processing logic (AI + DB) in a `try/except` block.
- **AI Failures**: Log error, keep status as `PENDING` (implicit by not updating), and `continue`.
- **Database Failures**: Log error, ensure session is closed, and `continue`.
- **Connection Safety**: Use context managers for every session.

### 4. Validation Strategy
- **Unit Test**: Test the mapping from Kafka JSON to `SupportTicket` model.
- **Integration Test**: Mock `AIAgent.process_ticket` and verify the database update happens correctly in `main_worker.py`.
- **End-to-End**: Run the worker and produce a message to the topic. Check `ticket` table state via SQL.
