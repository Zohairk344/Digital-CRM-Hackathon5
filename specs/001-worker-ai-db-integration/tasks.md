---

description: "Actionable tasks for Feature 4.2: Worker & DB Integration"
---

# Tasks: Worker & DB Integration (Feature 4.2)

**Input**: Design documents from `specs/001-worker-ai-db-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Integration tests are included in Phase 3 and 4 to ensure the worker's behavioral correctness.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Project**: `backend/`
- **Source**: `backend/app/`
- **Tests**: `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify backend environment and dependencies (uv) in `backend/pyproject.toml`
- [x] T002 [P] Verify Kafka broker and PostgreSQL availability via `docker-compose.yml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Update `Ticket` model with AI analysis fields (category, sentiment, suggested_response, is_escalated) in `backend/app/db/models.py`
- [x] T004 [P] Verify database initialization with new schema by running `backend/app/db/init_db.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Automated Ticket Enrichment (Priority: P1) 🎯 MVP

**Goal**: Automatically analyze and categorize incoming support tickets in the database.

**Independent Test**: Send a test ticket message to Kafka, wait for processing, and verify the `ticket` table is updated with `AI_PROCESSED` status and AI analysis data.

### Implementation for User Story 1

- [x] T005 [P] [US1] Add imports for `AIAgent`, `SupportTicket`, `AsyncSessionLocal`, and `Ticket` in `backend/app/workers/main_worker.py`
- [x] T006 [US1] Initialize `AIAgent` instance in `main()` function of `backend/app/workers/main_worker.py`
- [x] T007 [US1] Implement message parsing and `ticket_id` extraction logic in `backend/app/workers/main_worker.py`
- [x] T008 [US1] Implement database fetch for `Ticket` and associated `Message` context in `backend/app/workers/main_worker.py`
- [x] T009 [US1] Implement AI invocation using `agent.process_ticket(ticket_input)` in `backend/app/workers/main_worker.py`
- [x] T010 [US1] Implement database update for the `Ticket` record with AI results in `backend/app/workers/main_worker.py`
- [x] T011 [US1] Set ticket status to `AI_PROCESSED` upon successful database commit in `backend/app/workers/main_worker.py`
- [x] T012 [US1] Implement metadata-only logging for successful processing in `backend/app/workers/main_worker.py`

**Checkpoint**: User Story 1 functional - incoming tickets are now automatically enriched.

---

## Phase 4: User Story 2 - Resilient Message Processing (Priority: P2)

**Goal**: Ensure the Kafka worker remains operational despite intermittent AI service or database errors.

**Independent Test**: Simulate an AI service timeout and verify that the worker logs the error and continues to the next message without exiting.

### Implementation for User Story 2

- [x] T013 [US2] Wrap AI processing and DB transaction in a global `try/except` block in `backend/app/workers/main_worker.py`
- [x] T014 [US2] Implement 3-attempt exponential backoff retry for transient database conflicts in `backend/app/workers/main_worker.py`
- [x] T015 [US2] Implement error logging for failed processing attempts while ensuring loop `continue` in `backend/app/workers/main_worker.py`
- [x] T016 [US2] Ensure database sessions are explicitly closed in the `finally` block or via context manager in `backend/app/workers/main_worker.py`

**Checkpoint**: User Story 2 functional - worker is now resilient to transient failures.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T017 [P] Update `specs/001-worker-ai-db-integration/quickstart.md` with end-to-end verification steps
- [x] T018 Run comprehensive integration tests in `backend/tests/workers/test_integration.py`
- [x] T019 [P] Clean up temporary reproduction script `backend/tests/workers/reproduce_worker_state.py`
- [x] T020 [P] Documentation cleanup and cross-reference check in `specs/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational completion.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Foundation ready - No dependencies on other stories.
- **User Story 2 (P2)**: Depends on US1 implementation (the logic to wrap in try/except).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Implement User Story 1 (Tasks T005 - T012).
3. **STOP and VALIDATE**: Verify ticket enrichment works correctly.

### Incremental Delivery

1. Foundation ready.
2. Add enrichment logic (US1) -> Verify.
3. Add resilience and retry logic (US2) -> Verify error handling.
4. Final polish and documentation.
