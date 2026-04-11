# Quickstart: Worker & DB Integration

## Setup
1. Ensure the `Ticket` model in `backend/app/db/models.py` has been updated with `category`, `sentiment`, `suggested_response`, and `is_escalated` fields.
2. Initialize the database schema:
   ```bash
   cd backend
   uv run app/db/init_db.py
   ```
3. Ensure the `GOOGLE_API_KEY` is correctly configured in `backend/.env`.

## Execution
1. Start the Kafka worker:
   ```bash
   cd backend
   uv run app/workers/main_worker.py
   ```
2. In a separate terminal, produce a test ticket to Kafka. You can use the provided reproduction script:
   ```bash
   cd backend
   uv run tests/workers/reproduce_worker_state.py
   ```

## Verification
1. Check the worker logs for "Ticket processed and database updated successfully" with the `ticket_id`.
2. Use a database client to verify the `ticket` record has been updated:
   ```sql
   SELECT id, category, sentiment, status, is_escalated FROM ticket WHERE id = '<ticket_id>';
   ```
   Expect `status` to be `AI_PROCESSED` and analysis fields to be populated.
