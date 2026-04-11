# Implementation Plan: Web Support Form Channel

**Branch**: `052-web-support-form` | **Date**: 2026-03-28 | **Spec**: [specs/052-web-support-form/spec.md](spec.md)
**Input**: Feature specification from `/specs/052-web-support-form/spec.md`

## Summary
Implement a standalone Web Support Form channel consisting of a Next.js client component and a FastAPI backend webhook. The system will capture customer support requests, ensure atomic database persistence (Customer, Ticket, Message, OutboxEvent), and provide real-time submission feedback.

## Technical Context

**Language/Version**: Python 3.12+, TypeScript 5.x  
**Primary Dependencies**: FastAPI, Pydantic v2, Next.js 14+ (App Router), Tailwind CSS, Lucide React  
**Storage**: PostgreSQL (SQLAlchemy Async)  
**Testing**: pytest (Backend)  
**Target Platform**: Linux Server (Containerized)
**Project Type**: Web application (Full-stack)  
**Performance Goals**: < 2s submission latency, < 200ms p95 API response.  
**Constraints**: CORS restricted to `localhost:3000`, atomic database transactions mandatory.  
**Scale/Scope**: Primary contact channel for web visitors.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Role & Autonomy**: Is the architect role fully assumed? (Lead Digital FTE Architect)
- [x] **II. Technical Stack Sovereignty**: Are Python 3.12+, uv, FastAPI, Next.js, and Redpanda used?
- [x] **III. Architectural Standards**: Is the monorepo (/backend, /frontend, /infra) structure followed? Is it event-driven?
- [x] **IV. Business Logic Constraints**: Are the FTE Handbook rules (pricing, sentiment, channel limits) integrated?
- [x] **V. Coding Style & Safety**: Are strict types and robust error handling planned?
- [x] **VI. Operational Procedure**: Is the Web Support Form prioritized? Is the plan explained step-by-step?

## Project Structure

### Documentation (this feature)

```text
specs/052-web-support-form/
├── plan.md              # This file
├── research.md          # Research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
├── contracts/           # API Contract (OpenAPI)
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── webhooks/
│   │           └── web_form.py  # NEW: Web form webhook
│   ├── core/
│   │   └── sentiment.py         # NEW: Sentiment utility
│   └── main.py                  # MODIFIED: CORS & Router registration
└── tests/
    └── api/v1/
        └── test_web_form.py     # NEW: API integration tests

frontend/
├── src/
│   ├── components/
│   │   └── SupportForm.tsx      # NEW: Form component
│   └── app/
│       └── support/
│           └── page.tsx         # NEW: Support page
└── tests/
```

**Structure Decision**: Monorepo structure with FastAPI backend and Next.js frontend as per Constitution.

## File Tree Changes

### Created Files
- `backend/app/api/v1/webhooks/web_form.py`: FastAPI endpoint for web form submission.
- `backend/app/core/sentiment.py`: Simple sentiment analysis utility.
- `backend/tests/api/v1/test_web_form.py`: Integration tests for the new endpoint.
- `frontend/src/components/SupportForm.tsx`: React client component for the form.
- `frontend/src/app/support/page.tsx`: Page hosting the support form.

### Modified Files
- `backend/app/main.py`: Add CORSMiddleware and include the new webhook router.

## Dependency Management
- **Backend**: No new dependencies (using core FastAPI/Pydantic).
- **Frontend**: `npm install lucide-react` (for UI icons).

## Step-by-Step Implementation Logic

### Phase A: Backend CORS & Routing
1. Update `backend/app/main.py` to include `CORSMiddleware`.
2. Configure `allow_origins=["http://localhost:3000"]`.
3. Register the `v1/webhooks/web_form` router in the main app.

### Phase B: FastAPI Endpoint (`web_form.py`)
1. **Schema**: Define `WebFormSubmission` Pydantic model (name, email, phone, category, priority, message).
2. **Logic**:
   - Initialize `async with db.begin():` for atomic transaction.
   - **Sentiment**: Call `get_sentiment_score(message)`.
   - **Escalation**: Apply **FR-C1** (Pricing/Competitor keywords) and **FR-C2** (Sentiment < 0.3) logic to set priority to `urgent` and add tags.
   - **Customer**: `get_customer_by_email`. If missing, `create_customer` (store Name in `metadata_json` since model lacks name field).
   - **Ticket**: `create_ticket` linked to customer, `channel_origin='web'`.
   - **Message**: `create_message` linked to ticket, `sender_type='customer'`.
   - **Outbox**: `create_outbox_event` with type `ticket.created`.
   - Return `201 Created` with `ticket_id`.

### Phase C: Frontend UI Component (`SupportForm.tsx`)
1. Create a responsive form using Tailwind CSS.
2. **State**: Manage `formData`, `isSubmitting`, `successMessage`, and `errorMessage`.
3. **Fields**: Implement inputs for Name, Email, Phone, and Select for Category/Priority.
4. **Icons**: Use `lucide-react` for visual feedback.

### Phase D: Frontend Integration
1. Implement `handleSubmit` using native `fetch`.
2. Send `POST` to `http://localhost:8000/api/v1/webhooks/web-form`.
3. On success: Display `Ticket ID` and clear form.
4. On error: Display user-friendly error message.

## Validation Strategy
1. **Automated**: Run `pytest` on the new integration test file.
2. **Manual**: 
   - Start backend (`fastapi dev`).
   - Start frontend (`npm run dev`).
   - Submit a test ticket via `localhost:3000/support`.
   - Verify Ticket ID display and database record presence.
