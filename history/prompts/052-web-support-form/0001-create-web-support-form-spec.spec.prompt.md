---
id: 0001
title: Create Web Support Form Spec
stage: spec
date: 2026-03-28
surface: agent
model: gemini-cli
feature: 052-web-support-form
branch: 052-web-support-form
user: zohai
command: /sp.specify
labels: [spec, feature, nextjs, fastapi]
links:
  spec: specs/052-web-support-form/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/052-web-support-form/spec.md
 - specs/052-web-support-form/checklists/requirements.md
tests:
 - (none)
---

## Prompt

Build "Feature 2: Web Support Form Channel". This feature includes a standalone Next.js frontend component where customers can submit support requests, and a FastAPI backend endpoint to process these submissions. The backend must use the previously built CRUD operations to safely store the incoming request in the PostgreSQL database. [TECH STACK] - Frontend: Next.js 14+ (App Router), TypeScript, Tailwind CSS. - Backend: FastAPI (Python 3.12+), SQLAlchemy (Async), Pydantic v2. - Package Managers: npm (Frontend), uv (Backend). [FRONTEND REQUIREMENTS (Next.js)] 1. **SupportForm Component:** Create a modern, responsive React client component (SupportForm.tsx). 2. **Form Fields:** - Name (Text, required) - Email (Email, required) - *Crucial for cross-channel identification* - Phone (Tel, optional) - Category (Select/Dropdown: 'General', 'Bug Report', 'Feature Request', 'Billing') - Priority (Select/Dropdown: 'low', 'medium', 'high') - Message (Textarea, required) 3. **UX/UI State:** - Handle loading states (disable submit button, show spinner). - Display success message containing the newly created Ticket ID upon successful submission. - Display clear error messages if the submission fails. [BACKEND REQUIREMENTS (FastAPI)] 1. **API Endpoint:** Create a POST /api/v1/webhooks/web-form endpoint in FastAPI. 2. **Data Validation:** Create a Pydantic schema (WebFormSubmission) to validate the incoming JSON payload from the frontend. 3. **Database Operations (using existing crud.py):** - **Customer:** Look up the customer by email. If they don't exist, create a new Customer record. - **Ticket:** Create a new Ticket linked to the customer. Set channel_origin to 'web' and status to 'open'. - **Message:** Create a new Message linked to the ticket containing the user's text. Set sender_type to 'customer' and channel to 'web'. - **Outbox/Kafka Prep:** If an OutboxEvent model exists from Feature 1, log this new ticket creation as an event so the Kafka producer can pick it up later. 4. **Response:** Return the created ticket_id and a success status to the frontend. [EDGE CASES & CORS] - **CORS:** Ensure the FastAPI app has CORSMiddleware configured to accept requests from the Next.js local development server (typically http://localhost:3000). - **Database Rollbacks:** The endpoint must execute the Customer, Ticket, and Message creation within a single asynchronous database transaction. If any step fails, the entire transaction must roll back to prevent orphaned records.

## Response snapshot

Successfully created the feature specification and quality checklist for 'Web Support Form Channel'. The new feature branch is `052-web-support-form`. The specification is located at `specs/052-web-support-form/spec.md`. The feature is ready for the next phase: `/sp.plan`.

## Outcome

- ✅ Impact: High - core web support channel defined.
- 🧪 Tests: No tests run; requirements for testing defined in spec.
- 📁 Files: Created `specs/052-web-support-form/spec.md` and `specs/052-web-support-form/checklists/requirements.md`.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The specification correctly handles both frontend components and backend endpoints, ensuring atomic database operations and clear UX feedback.

## Evaluation notes (flywheel)

- Failure modes observed: (none)
- Graders run and results (PASS/FAIL): (none)
- Prompt variant (if applicable): (none)
- Next experiment (smallest change to try): (none)
