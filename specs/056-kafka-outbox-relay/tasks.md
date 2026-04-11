# Tasks: Kafka Producer & Outbox Relay (Outbound Event Streaming)

**Input**: Design documents from `specs/056-kafka-outbox-relay/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

---

## Phase 1: Setup (Dependencies)

**Purpose**: Project initialization and dependency management.

- [X] T001 [P] Install `aiokafka` dependency in `backend/`
  - **Environment:** Backend (`uv`)
  - **Action:** `uv add aiokafka`
  - **Target File(s):** `backend/pyproject.toml`
  - **Details:** Add the async Kafka client to the backend virtual environment.
  - **Verification:** Run `uv run python -c "import aiokafka"` to ensure successful installation.

- [X] T002 [P] Verify Kafka settings in `backend/app/core/config.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Ensure `KAFKA_BROKER_URL` and `KAFKA_TOPIC_SUPPORT_TICKETS` are correctly defined in the `Settings` class.
  - **Target File(s):** `backend/app/core/config.py`
  - **Details:** Settings should default to `localhost:9092` and `support.tickets.new`.
  - **Verification:** Run a small script to print `settings.KAFKA_BROKER_URL`.

- [X] T003 [P] Add `KAFKA_BROKER_URL` to `backend/.env`
  - **Environment:** Backend (`uv`)
  - **Action:** Add `KAFKA_BROKER_URL=localhost:9092` to the environment file.
  - **Target File(s):** `backend/.env`
  - **Details:** Ensure the environment variable is available for the application.
  - **Verification:** `cat backend/.env` to confirm entry.

---

## Phase 2: Foundational (Producer Client & Models)

**Purpose**: Core infrastructure required for all user stories.

- [X] T004 [P] Update `OutboxEvent` model in `backend/app/db/models.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Ensure `retry_count` and `status` fields are present and correctly typed.
  - **Target File(s):** `backend/app/db/models.py`
  - **Details:** `retry_count` (Integer, default=0), `status` (String, default='pending').
  - **Verification:** Check the model definition against the `data-model.md` design.

- [X] T005 [P] Implement `KafkaProducer` wrapper in `backend/app/core/kafka_producer.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Create an `AIOKafkaProducer` wrapper class.
  - **Target File(s):** `backend/app/core/kafka_producer.py`
  - **Details:** Implement `start()`, `stop()`, and `send_message(topic, payload)` with basic error handling.
  - **Verification:** Instantiate the class in a test script and attempt `start()` (mocking broker if necessary).

- [X] T006 [P] Define `run_outbox_relay` shell in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Create the background loop structure with `asyncio.sleep(5)`.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Create a while loop that will eventually host the polling logic.
  - **Verification:** Ensure the script can be imported without errors.

---

## Phase 3: User Story 1 - Automated Event Streaming (Priority: P1) 🎯 MVP

**Goal**: Automatically stream new webhook submissions from the database to a message broker.

**Independent Test**: Manually insert a record into the `OutboxEvent` table and verify it appears in the Kafka topic and is subsequently marked as processed in the database.

- [X] T007 [US1] Implement DB polling logic in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Implement fetching `pending` events (limit 50, FIFO) using `AsyncSessionLocal`.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Use `created_at` for FIFO ordering.
  - **Verification:** Log the number of events fetched in each iteration.

- [X] T008 [US1] Integrate `KafkaProducer.send_message` in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Call the producer to send the payload of each fetched event.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Ensure the payload is serialized if necessary (JSON).
  - **Verification:** Check Kafka topic for messages using `rpk` or equivalent.

- [X] T009 [US1] Implement "At-least-once" delivery logic in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Update `status` to `processed` only after successful Kafka ACK.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Commit the database transaction after each successful publish.
  - **Verification:** Verify `status` in `outbox_event` table changes to `processed`.

- [X] T010 [US1] Add success logging in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Log successful event transmissions with event ID.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Use standard Python `logging`.
  - **Verification:** Check application logs for success messages.

---

## Phase 4: User Story 2 - Resilient Message Delivery (Priority: P2)

**Goal**: Handle temporary message broker outages gracefully.

**Independent Test**: Stop the Redpanda broker, add an outbox event, verify the relay logs the failure but keeps running, then start Redpanda and verify the event is eventually delivered.

- [X] T011 [US2] Implement exponential backoff in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Add backoff logic for when the broker is unavailable.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Prevent tight loop failures when the broker is down.
  - **Verification:** Observe logs during simulated broker outage.

- [X] T012 [US2] Implement poison message limit in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Update `status` to `failed` after 3 unsuccessful attempts.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Increment `retry_count` on failure.
  - **Verification:** Manually create a failing event and verify it reaches `failed` status after 3 tries.

- [X] T013 [US2] Add detailed error logging in `backend/app/core/outbox_relay.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Log failure reason and event ID.
  - **Target File(s):** `backend/app/core/outbox_relay.py`
  - **Details:** Ensure observability for troubleshooting.
  - **Verification:** Check logs for failure details.

---

## Phase 5: User Story 3 - Clean System Lifecycle (Priority: P3)

**Goal**: Start and stop the event producer cleanly with the application.

**Independent Test**: Start the application and check logs for successful connection, then stop the application and verify clean shutdown.

- [X] T014 [US3] Implement `@asynccontextmanager` lifespan in `backend/app/main.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Update `app/main.py` to use a lifespan context manager.
  - **Target File(s):** `backend/app/main.py`
  - **Details:** Manage startup and shutdown events centrally.
  - **Verification:** Ensure the app starts and stops without errors.

- [X] T015 [US3] Start relay and producer in lifespan startup in `backend/app/main.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Call `producer.start()` and `asyncio.create_task(run_outbox_relay())`.
  - **Target File(s):** `backend/app/main.py`
  - **Details:** Ensure the background task starts when the app starts.
  - **Verification:** Check logs for startup messages from the relay and producer.

- [X] T016 [US3] Gracefully stop relay and producer in lifespan shutdown in `backend/app/main.py`
  - **Environment:** Backend (`uv`)
  - **Action:** Cancel the relay task and call `producer.stop()`.
  - **Target File(s):** `backend/app/main.py`
  - **Details:** Ensure clean resource release.
  - **Verification:** Check logs for clean shutdown messages; measure shutdown duration to confirm it is < 2 seconds (per SC-004).


---

## Phase 6: Polish & E2E Verification

**Purpose**: Final audit and end-to-end testing.

- [X] T017 [P] Audit log levels in `backend/app/core/`
  - **Environment:** Backend (`uv`)
  - **Action:** Ensure consistent and appropriate logging levels (INFO, ERROR).
  - **Target File(s):** `backend/app/core/kafka_producer.py`, `backend/app/core/outbox_relay.py`
  - **Verification:** Review logs during a full run.

- [X] T018 [P] Documentation updates in `specs/056-kafka-outbox-relay/quickstart.md`
  - **Environment:** Backend (`uv`)
  - **Action:** Update the quickstart with any new details or verification steps.
  - **Target File(s):** `specs/056-kafka-outbox-relay/quickstart.md`
  - **Verification:** Read through the document for accuracy.

- [X] T019 E2E Verification: Submit web form and verify Kafka delivery
  - **Environment:** Backend (`uv`)
  - **Action:** Trigger the full flow: Webhook -> DB -> Relay -> Kafka.
  - **Target File(s):** `backend/app/api/v1/webhooks/web_form.py` (via API)
  - **Details:** Use the existing web support form endpoint to create an event.
  - **Verification:** Confirm message reaches Kafka and `outbox_event` is marked `processed`.


---

## Dependencies & Execution Order

### Phase Dependencies
- Phase 1 (Setup) must be completed first.
- Phase 2 (Foundational) depends on Phase 1.
- Phase 3, 4, 5 (User Stories) depend on Phase 2.
- Phase 6 (Polish) depends on all User Stories.

### Parallel Opportunities
- Tasks marked with [P] within the same phase can be executed in parallel.
- Phase 3 and 4 have shared dependencies in `outbox_relay.py` and should be implemented sequentially.

---

## Implementation Strategy
- **MVP First**: Complete Phase 1, 2, and 3 to have a working outbound stream.
- **Incremental Delivery**: Add Phase 4 for resilience and Phase 5 for proper lifecycle management.
