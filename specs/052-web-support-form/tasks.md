# Tasks: Web Support Form Channel

**Input**: Design documents from `/specs/052-web-support-form/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included for backend integration and data integrity verification as requested in the implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Configure CORSMiddleware to allow origins from `http://localhost:3000` in `backend/app/main.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Update `main.py` with CORS configuration.
  - **Verification**: Run backend and check headers or verify with a simple curl/fetch from different origin.
- [x] T002 [P] Install frontend dependencies (`lucide-react`) in `frontend/`
  - **Environment**: Frontend (`npm`)
  - **Action**: Run `npm install lucide-react`.
  - **Verification**: Check `package.json` for the new dependency.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 Implement basic sentiment analysis utility in `backend/app/core/sentiment.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Create `sentiment.py` with a heuristic that returns 0.1 if text contains "angry", "broken", "terrible", or "urgent", otherwise 1.0.
  - **Verification**: Write a small script to call the function and verify output.
- [x] T004 Create and register the webhook router in `backend/app/main.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Create `backend/app/api/v1/webhooks/web_form.py` (empty router) and register it in `main.py`.
  - **Verification**: Backend starts without errors.

---

## Phase 3: User Story 1 - Customer Submits a Web Support Request (Priority: P1) 🎯 MVP

**Goal**: Enable customers to submit a basic support form and receive a Ticket ID.

**Independent Test**: Fill out form -> Submit -> Receive Ticket ID -> Verify record in DB.

### Implementation for User Story 1

- [x] T005 [US1] Define `WebFormSubmission` Pydantic schema in `backend/app/api/v1/webhooks/web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Add Pydantic model with fields from spec (Name, Email, etc.).
  - **Verification**: Pydantic validation passes for valid JSON payload.
- [x] T006 [US1] Implement core `POST /api/v1/webhooks/web-form` endpoint in `backend/app/api/v1/webhooks/web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Implement logic to create Customer, Ticket, and Message using existing CRUD.
  - **Verification**: Use Postman/curl to submit a request and receive a 201 response with `ticket_id`.
- [x] T007 [P] [US1] Create basic `SupportForm.tsx` component structure in `frontend/src/components/SupportForm.tsx`
  - **Environment**: Frontend (`npm`)
  - **Action**: Build form layout with fields: Name, Email, Phone, Category, Priority, Message.
  - **Verification**: Component renders correctly in a dev server.
- [x] T008 [P] [US1] Create support page route in `frontend/src/app/support/page.tsx`
  - **Environment**: Frontend (`npm`)
  - **Action**: Create page file and import/render `SupportForm`.
  - **Verification**: Navigate to `/support` and see the form.
- [x] T009 [US1] Implement `handleSubmit` with native `fetch` in `frontend/src/components/SupportForm.tsx`
  - **Environment**: Frontend (`npm`)
  - **Action**: Hook up form submission to backend endpoint.
  - **Verification**: Submit form and see the raw response or alert with `ticket_id`.

**Checkpoint**: At this point, the core flow from frontend to backend is functional.

---

## Phase 4: User Story 2 - Form Validation and User Feedback (Priority: P2)

**Goal**: Provide clear validation and UX feedback to the user.

**Independent Test**: Attempt invalid submission -> See error -> Submit valid -> See loading -> See success.

### Implementation for User Story 2

- [x] T010 [US2] Add client-side validation and loading states to `frontend/src/components/SupportForm.tsx`
  - **Environment**: Frontend (`npm`)
  - **Action**: Implement email format check and required field validation; manage `isSubmitting` state.
  - **Verification**: Submit button disables during fetch; errors show for empty fields.
- [x] T011 [US2] Implement success and error UI messages in `frontend/src/components/SupportForm.tsx`
  - **Environment**: Frontend (`npm`)
  - **Action**: Show success message with `ticket_id` on success; show error toast/message on failure.
  - **Verification**: Visual confirmation of success/error banners.

---

## Phase 5: User Story 3 - System Resilience and Data Integrity (Priority: P3)

**Goal**: Ensure data atomicity and handle edge cases like sentiment escalation.

**Independent Test**: Simulate failure -> Verify no partial DB records -> Submit negative text -> Verify urgent priority.

### Implementation for User Story 3

- [x] T012 [US3] Refactor endpoint to use `async with db.begin():` for atomic transaction in `backend/app/api/v1/webhooks/web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Ensure Customer, Ticket, and Message creation are within a single transaction block.
  - **Verification**: Intentionally raise an exception after Ticket creation; verify no records exist in DB.
- [x] T013 [US3] Implement sentiment and pricing escalation logic in `backend/app/api/v1/webhooks/web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Apply **FR-C1** and **FR-C2** rules to update priority and tags.
  - **Verification**: Submit a message with "pricing" and verify ticket is created with 'high' priority.
- [x] T014 [US3] Implement `OutboxEvent` logging in `backend/app/api/v1/webhooks/web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Add `create_outbox_event` call within the transaction.
  - **Verification**: Check `outbox_event` table after submission.
- [x] T015 [P] [US3] Create integration tests in `backend/tests/api/v1/test_web_form.py`
  - **Environment**: Backend (`uv`)
  - **Action**: Write pytest scenarios for success, validation error, and transaction rollback.
  - **Verification**: Run `pytest backend/tests/api/v1/test_web_form.py` and see all pass.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation.

- [x] T016 Run `quickstart.md` validation steps
- [x] T017 Final manual E2E test from Frontend browser to Backend DB
- [x] T018 Code cleanup and type hint verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Depends on US1 UI component existence.
- **User Story 3 (P3)**: Depends on US1 Backend logic existence.

### Parallel Opportunities

- T001 (Backend) and T002 (Frontend)
- T003 (Backend) and T007/T008 (Frontend)
- T015 (Tests) can be written in parallel with T012/T013.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Complete Phase 3 (US1).
3. **STOP and VALIDATE**: Verify a basic form submission creates a ticket.

### Incremental Delivery

1. Add Phase 4 (US2) for better UX.
2. Add Phase 5 (US3) for production-grade reliability and business rules.
