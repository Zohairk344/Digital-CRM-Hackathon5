# Quickstart: Kafka Outbox Relay

## Prerequisites
- Redpanda (Kafka) running on `localhost:9092`.
- Backend virtual environment initialized with `uv`.
- PostgreSQL database populated with the `outbox_event` table.

## Step 1: Install Dependencies
```bash
cd backend
uv add aiokafka
```

## Step 2: Configure Environment
Ensure `backend/.env` contains the following:
```env
KAFKA_BROKER_URL=localhost:9092
```

## Step 3: Run the Application
The relay task starts automatically with the FastAPI application using the `lifespan` event.
```bash
cd backend
uv run uvicorn app.main:app --reload
```

## Step 4: Verification
1. **Trigger an Event**: Submit a web support form or manually insert a record into the `outbox_event` table.
   ```sql
   INSERT INTO outbox_event (id, event_type, payload, status, created_at) 
   VALUES (gen_random_uuid(), 'ticket.created', '{"ticket_id": 123, "customer": "John Doe"}', 'pending', now());
   ```
2. **Observe Logs**: Check application logs for messages indicating successful Kafka publishing:
   `INFO: Successfully published event {id} to topic support.tickets.new`
3. **Verify DB Update**: Check the database to confirm the record is marked as `processed`.
   ```sql
   SELECT id, status FROM outbox_event WHERE id = '{your_event_id}';
   ```
4. **Inspect Topic (Optional)**: Using `rpk` or any Kafka UI, verify the message is present in the topic `support.tickets.new`.
