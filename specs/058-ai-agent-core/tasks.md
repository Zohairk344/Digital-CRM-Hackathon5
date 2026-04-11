# Tasks: AI Agent Core (Feature 4.1)

**Input**: Design documents from `/specs/058-ai-agent-core/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dependency installation and basic module structure

- [x] T001 Install AI Libraries in backend/pyproject.toml
    - **Environment:** Backend (`uv`)
    - **Action:** Add `langchain`, `langchain-google-genai`, and `pydantic` to the backend.
    - **Target File(s):** `backend/pyproject.toml`
    - **Details:** Run `uv add langchain langchain-google-genai pydantic` in the `/backend` directory.
    - **Verification:** Check `pyproject.toml` or run `uv lock` to confirm dependencies are present.

- [x] T002 [P] Create module initialization in backend/app/ai/__init__.py
    - **Environment:** Backend (`uv`)
    - **Action:** Create an empty `__init__.py` to make the directory a Python package.
    - **Target File(s):** `backend/app/ai/__init__.py`
    - **Details:** Ensure the `app/ai` directory exists and contains `__init__.py`.
    - **Verification:** Confirm file existence via `ls backend/app/ai/__init__.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logic initialization

- [x] T003 [US1] Define Pydantic schema in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Create `SupportTicket` (input) and `TicketAnalysis` (output) Pydantic models.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** 
        - Define `SupportTicket` model with: `ticket_id`, `subject`, `description`.
        - Define `CategoryEnum` and `SentimentLabelEnum`.
        - Define `TicketAnalysis` model with: `category`, `sentiment_label`, `sentiment_score`, `is_escalated`, and `suggested_response`.
    - **Verification:** Run a schema check script to ensure both models are importable and valid.

---

## Phase 3: User Story 1 - AI-Powered Ticket Analysis (Priority: P1) 🎯 MVP

**Goal**: Analyze tickets for category, sentiment, and response.

**Independent Test**: Run the script with a mock ticket and see structured output for category and sentiment.

- [x] T004 [US1] Initialize Gemini LLM in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Initialize `ChatGoogleGenerativeAI(model="gemini-1.5-flash")`.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** Setup the LLM instance. Ensure it reads `GOOGLE_API_KEY` from the environment.
    - **Verification:** Confirm logic allows for initialization without hardcoded keys.

- [x] T005 [US1] Create ChatPromptTemplate in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Define the system and human messages.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** 
        - System Message: "You are an expert customer support agent..." 
        - Human Message: Pass `ticket_id`, `subject`, and `description`.
    - **Verification:** Confirm prompt contains instructions for concise, bullet-point responses.

- [x] T006 [US1] Implement process_ticket chain logic in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Combine prompt and LLM with structured output.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** Use `llm.with_structured_output(TicketAnalysis)` and create the `process_ticket(payload: dict) -> TicketAnalysis` function.
    - **Verification:** Logic exists to invoke the chain and return the parsed model.

---

## Phase 4: User Story 2 - Automated Escalation Detection (Priority: P2)

**Goal**: Flag tickets for human intervention based on rules.

**Independent Test**: Use a ticket with "pricing" or bad sentiment and verify `is_escalated` is `True`.

- [x] T007 [US2] Implement escalation logic for pricing and sentiment in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Add logic to enforce Constitution rules for escalation.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** 
        - Instruct LLM to detect pricing/competitors.
        - Add a secondary Python check: If `sentiment_score < 0.3`, force `is_escalated = True`.
    - **Verification:** Verify `process_ticket` returns `is_escalated=True` for a mock pricing query via logic tests.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and isolated testing block

- [x] T008 Implement isolated testing block in backend/app/ai/agent.py
    - **Environment:** Backend (`uv`)
    - **Action:** Add `if __name__ == "__main__":` block.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** Include a mock ticket payload and call `process_ticket`.
    - **Verification:** Confirm `python app/ai/agent.py` runs without error.

- [x] T009 Run execution test and verify output/performance
    - **Environment:** Backend (`uv`)
    - **Action:** Execute the agent script, inspect output, and measure time.
    - **Target File(s):** `backend/app/ai/agent.py`
    - **Details:** Run `uv run python -m app.ai.agent`.
    - **Verification:** Terminal prints valid Pydantic object AND logic tests pass. (Live Gemini test pending `GOOGLE_API_KEY`).

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1.
- **User Story 1 (Phase 3)**: Depends on Phase 2.
- **User Story 2 (Phase 4)**: Depends on Phase 3.
- **Polish (Phase 5)**: Depends on Phase 4.

### Parallel Opportunities
- T002 can be done alongside T001 if paths exist.
- T003, T004, T005 are mostly sequential within one file but T004/T005 can be drafted in parallel if needed.

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 & 2.
2. Complete US1 implementation.
3. Validate US1 with a neutral ticket.

### Incremental Delivery
1. Add US2 logic to the existing chain.
2. Add the main execution block for final verification.
