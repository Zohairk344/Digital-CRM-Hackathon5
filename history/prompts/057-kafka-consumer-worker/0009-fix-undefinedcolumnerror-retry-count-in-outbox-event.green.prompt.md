---
id: "0009"
title: "Fix UndefinedColumnError retry_count in outbox_event"
stage: "green"
date: "2026-04-04"
surface: "agent"
model: "gemini-2.0-pro-exp"
feature: "057-kafka-consumer-worker"
branch: "057-kafka-consumer-worker"
user: "zohai"
command: "/sp.implement"
labels: ["postgresql", "sqlalchemy", "outbox", "fix"]
links:
  spec: "specs/057-kafka-consumer-worker/spec.md"
  plan: "specs/057-kafka-consumer-worker/plan.md"
  tasks: "specs/057-kafka-consumer-worker/tasks.md"
files:
  - "backend/fix_db.py (temporary)"
tests:
  - "n/a (manual script execution)"
---

# Prompt

Fix the `UndefinedColumnError: column outbox_event.retry_count does not exist` error crashing the FastAPI outbox relay.

[EXECUTION PROTOCOL]
1. Change directory to `/backend`.
2. The `OutboxEvent` SQLAlchemy model was updated with a `retry_count` column, but the PostgreSQL database schema is out of sync.
3. **Fallback Fix (Direct SQL):** write a temporary Python script (`fix_db.py`) that connects to the database and executes `ALTER TABLE outbox_event ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0;`. Run the script, and then delete it.

# Response

I have fixed the `UndefinedColumnError` by adding the missing `retry_count` column to the `outbox_event` table in PostgreSQL.

### Execution Summary:
1.  **Analyzed Schema**: Verified that `backend/app/db/models.py` defines `retry_count` for the `OutboxEvent` model.
2.  **Identified Gap**: Confirmed that the database was out of sync with the model.
3.  **Applied Fix**:
    - Created a temporary script `backend/fix_db.py` using `sqlalchemy` and `asyncpg`.
    - Executed `ALTER TABLE outbox_event ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0;` using the system Python (which had the required libraries).
    - Verified the column was added successfully.
4.  **Cleanup**: Deleted the `fix_db.py` script.

The outbox relay background task should now be able to process events without crashing on the missing column.
