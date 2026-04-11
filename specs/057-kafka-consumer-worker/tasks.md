# Tasks: Standalone Kafka Consumer Worker

**Input**: Design documents from `/specs/057-kafka-consumer-worker/`
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`

## Phase 1: Setup (Project Initialization)

**Purpose**: Establish directory structure and install required dependencies.

- [x] T001 Create worker directory structure in `backend/app/workers/`
  - **Environment**: Backend (uv)
  - **Action**: Create the directory `backend/app/workers/` and an empty `backend/app/workers/__init__.py` file.
  - **Target File(s)**: `backend/app/workers/__init__.py`
  - **Details**: Ensure the package structure is correct for standalone execution.
  - **Verification**: Run `ls backend/app/workers/` and verify both the directory and `__init__.py` exist.

- [x] T002 Install worker dependencies
  - **Environment**: Backend (uv)
  - **Action**: Use `uv add` to install `aiokafka`, `python-json-logger`, and `pydantic`.
  - **Target File(s)**: `backend/pyproject.toml`
  - **Details**: These dependencies are required for Kafka connectivity, structured logging, and data validation.
  - **Verification**: Run `uv lock` and check `pyproject.toml` for the added libraries.

---

## Phase 2: Foundational (Configuration & Entrypoint)

**Purpose**: Set up the environment loading, logging, and the main execution block.

- [x] T003 Implement environment configuration in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Load `KAFKA_BROKER_URL`, `KAFKA_TOPIC`, and `KAFKA_GROUP_ID` from environment variables using `os.getenv`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: Provide defaults as specified in the spec: `support.tickets.new` and `fte-ai-worker-group`.
  - **Verification**: Temporarily add a print statement to verify variables are loaded correctly when running the script.

- [x] T004 [P] Configure structured JSON logging in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Setup `logging` with `pythonjsonlogger.jsonlogger.JsonFormatter`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: Ensure all logs are output to stdout in a key-value JSON format.
  - **Verification**: Run the script and verify that log messages are printed as JSON strings.

- [x] T005 Create main entrypoint and loop wrapper in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Implement an `async def main()` function and the `if __name__ == "__main__":` block using `asyncio.run()`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: This provides the standalone execution capability without FastAPI.
  - **Verification**: Run `python -m app.workers.main_worker` and ensure it starts without errors (even if it does nothing yet).

**Checkpoint**: Foundation ready - the script can now be extended with Kafka consumer logic.

---

## Phase 3: User Story 1 - Process Support Tickets (Priority: P1) 🎯 MVP

**Goal**: Automatically consume and log incoming support ticket events.

**Independent Test**: Run the worker script, produce a test message to the topic via a separate script or Redpanda console, and verify the worker logs the Ticket ID and payload.

### Implementation for User Story 1

- [x] T006 [US1] Initialize AIOKafkaConsumer in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Instantiate `AIOKafkaConsumer` with the loaded URL, group ID, and `auto_offset_reset='earliest'`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: Configure the consumer to subscribe to the configured topic.
  - **Verification**: Ensure the worker connects successfully to Redpanda on startup.

- [x] T007 [US1] Implement the polling loop in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Write the `async for message in consumer:` loop to deserialize JSON and log the `ticket_id` and content.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: Follow the data model from `data-model.md`. Log malformed JSON and continue (Log and Skip).
  - **Verification**: Manually produce a message to the topic and check the worker logs for the expected JSON output.

- [x] T008 [P] [US1] Create integration test in `backend/tests/workers/test_main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Write a test using `pytest-asyncio` that mocks or uses a test Kafka topic to verify message consumption.
  - **Target File(s)**: `backend/tests/workers/test_main_worker.py`
  - **Details**: Verify that the processing logic correctly handles a valid `Support Ticket Event`.
  - **Verification**: Run `pytest backend/tests/workers/test_main_worker.py`.

**Checkpoint**: User Story 1 is functional. The worker can reliably consume and log messages.

---

## Phase 4: User Story 2 - Graceful Termination (Priority: P1)

**Goal**: Ensure the worker shuts down cleanly upon receiving OS signals.

**Independent Test**: Send `SIGINT` (Ctrl+C) or `SIGTERM` to the running process and verify the logs show a clean exit sequence.

### Implementation for User Story 2

- [x] T009 [US2] Implement signal handlers in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Use `asyncio.get_running_loop().add_signal_handler()` for `SIGINT` and `SIGTERM`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: The handlers should set an `asyncio.Event` to signal the loop to stop.
  - **Verification**: Log a message when a signal is received to verify the handler is triggered.

- [x] T010 [US2] Implement clean shutdown logic in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: After the loop breaks, call `await consumer.stop()` and log the final shutdown status.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: This ensures offsets are committed and connections are closed cleanly.
  - **Verification**: Run the worker, stop it with Ctrl+C, and verify the connection is closed in the Redpanda logs or via consumer group status.

- [x] T011 [P] [US2] Verify signal handling in integration tests
  - **Environment**: Backend (uv)
  - **Action**: Add a test case to `backend/tests/workers/test_main_worker.py` that simulates a shutdown signal.
  - **Target File(s)**: `backend/tests/workers/test_main_worker.py`
  - **Details**: Ensure the worker loop terminates correctly when the stop event is set.
  - **Verification**: Run `pytest backend/tests/workers/test_main_worker.py`.

---

## Phase 5: Polish & Finalization

**Purpose**: Final documentation and validation.

- [x] T012 [P] Update documentation and context
  - **Environment**: Backend (uv)
  - **Action**: Update `quickstart.md` with final execution instructions and `GEMINI.md` with the new worker role.
  - **Target File(s)**: `specs/057-kafka-consumer-worker/quickstart.md`, `GEMINI.md`
  - **Details**: Ensure future agents know how to run and interact with the worker.
  - **Verification**: Read the updated files to confirm accuracy.

- [x] T013 Fix KafkaConnectionError crash on startup in `backend/app/workers/main_worker.py`
  - **Environment**: Backend (uv)
  - **Action**: Wrap `await consumer.start()` in an asynchronous `while True` loop with a `try/except` block catching `aiokafka.errors.KafkaConnectionError`.
  - **Target File(s)**: `backend/app/workers/main_worker.py`
  - **Details**: If it fails, log a warning and `await asyncio.sleep(5)` before retrying.
  - **Verification**: Simulate broker unavailability and verify the worker retries instead of crashing.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)**: Must be completed first.
- **Phase 2 (Foundational)**: Depends on Phase 1.
- **Phase 3 (US1)**: Depends on Phase 2. This is the MVP.
- **Phase 4 (US2)**: Depends on Phase 3. Adds reliability.
- **Phase 5 (Polish)**: Final step after implementation.

### Implementation Strategy
1. **MVP**: Complete T001 through T007. Validate manually by producing messages.
2. **Reliability**: Add signal handling (T009-T010).
3. **Automated Testing**: Finalize tests (T008, T011).
