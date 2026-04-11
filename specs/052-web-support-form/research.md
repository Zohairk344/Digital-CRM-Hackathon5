# Research: Web Support Form Channel

## Technical Unknowns & Patterns

### 1. FastAPI CORSMiddleware Configuration
- **Decision**: Use `fastapi.middleware.cors.CORSMiddleware`.
- **Rationale**: Standard FastAPI approach for handling Cross-Origin Resource Sharing.
- **Alternatives considered**: Manual header injection (rejected as error-prone).
- **Implementation**: Configure `allow_origins=["http://localhost:3000"]`, `allow_methods=["*"]`, `allow_headers=["*"]`.

### 2. Next.js 14+ Fetch Patterns
- **Decision**: Use native `fetch` API within a React Client Component.
- **Rationale**: Built-in, no extra dependencies, fits Next.js App Router patterns.
- **Patterns**: Handle errors via `response.ok` check, use `useState` for loading/error/success states.

### 3. Sentiment Analysis Integration
- **Decision**: Use a lightweight sentiment analysis library or a simple heuristic if no ML model is available yet. For this plan, I will assume a utility function `get_sentiment_score(text)` will be used.
- **Rationale**: **FR-C2** requires sentiment-based escalation.
- **Patterns**: Calculate score before ticket creation to determine priority and tags.

### 4. Atomic Database Transactions in FastAPI
- **Decision**: Use `async with db.begin():` block in the endpoint.
- **Rationale**: Ensures all operations (Customer, Ticket, Message, Outbox) are committed or rolled back together, satisfying **FR-009**.
- **Refinement**: Since existing CRUD functions in `crud.py` call `await db.commit()`, I will either:
  a) Use the models directly in the endpoint logic.
  b) Wrap the CRUD calls in a transaction and handle the `commit` manually if I modify the CRUD signatures.
  *Preferred for Plan*: Use the ORM models directly within a single transaction block in the webhook endpoint to ensure strict atomicity without side effects from existing CRUD helpers.

## Dependencies to Add
- **Backend**: None (FastAPI and Pydantic are core).
- **Frontend**: `lucide-react` for icons.
