---
id: 0007
title: Update CRM DB Foundations Spec
stage: spec
date: 2026-03-24
surface: agent
model: Gemini-2.0-Flash
feature: 050-crm-db-foundations
branch: 050-crm-db-foundations
user: zohai
command: /sp.specify
labels: ["spec", "database", "crm", "foundations"]
links:
  spec: specs/050-crm-db-foundations/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/050-crm-db-foundations/spec.md
  - specs/050-crm-db-foundations/checklists/requirements.md
tests:
  - Specification Quality Checklist validation
---

## Prompt

Build the foundational Database configuration and SQLAlchemy ORM models for the CRM Digital FTE Factory. The goal is to establish the async connection to PostgreSQL and define the schema required to track cross-channel customers, support tickets, and individual messages, as well as a vector store for the knowledge base. [TECH STACK] - Framework: FastAPI (Python 3.12+) - ORM: SQLAlchemy 2.0 (Async) - Database Driver: asyncpg - Validation: Pydantic v2 - Extensions: pgvector (for knowledge base embeddings) - Package Manager: uv [DATA MODEL REQUIREMENTS] Create the following SQLAlchemy models using UUIDs for primary keys: 1. `Customer`: - `id`: UUID (Primary Key) - `email`: String (Unique, Nullable) - Used for Gmail/Web - `phone`: String (Unique, Nullable) - Used for WhatsApp - `created_at`: DateTime (UTC) *Note: Either email or phone must be present to identify the user.* 2. `Ticket`: - `id`: UUID (Primary Key) - `customer_id`: UUID (Foreign Key) - `status`: Enum ('open', 'in_progress', 'resolved', 'escalated') - `priority`: Enum ('low', 'medium', 'high') - `channel_origin`: Enum ('web', 'gmail', 'whatsapp') - `created_at` / `updated_at`: DateTime (UTC) 3. `Message`: - `id`: UUID (Primary Key) - `ticket_id`: UUID (Foreign Key) - `sender_type`: Enum ('customer', 'agent') - `channel`: Enum ('web', 'gmail', 'whatsapp') - `content`: Text (The actual message) - `sentiment_score`: Float (Nullable, 0.0 to 1.0) - `created_at`: DateTime (UTC) 4. `KnowledgeArticle`: - `id`: UUID (Primary Key) - `title`: String - `content`: Text - `embedding`: Vector (Using pgvector, size depends on the chosen embedding model, default to 1536 for OpenAI `text-embedding-3-small`) [FUNCTIONALITY & STATE] - Create a `database.py` file that sets up the `AsyncEngine` and `async_sessionmaker`. - Use environment variables (via a `config.py` using Pydantic `BaseSettings`) to construct the database URL (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.). - Create a `models.py` file containing the declarative base and the four models defined above. Ensure relationships (`relationship()`) are properly mapped (e.g., a Customer has many Tickets). [EDGE CASES & ERROR HANDLING] - Connection Drops: Ensure the engine is configured with appropriate pool pre-ping settings to handle potential database disconnects gracefully. - Nullability: Enforce database-level constraints where a `Customer` cannot be created if both `email` and `phone` are null.

## Response snapshot

Updated the feature specification for `050-crm-db-foundations` to incorporate the detailed technical and functional requirements for the CRM database foundations. Translated implementation-specific details into technology-agnostic functional requirements while ensuring all core entities (Customer, Ticket, Message, KnowledgeArticle) and constraints (UUID PKs, email/phone nullability, vector embeddings) are correctly captured. Created a quality checklist at `specs/050-crm-db-foundations/checklists/requirements.md` and validated the specification.

## Outcome

- ✅ Impact: Established clear functional requirements and success criteria for the CRM database layer.
- 🧪 Tests: Validated against the Specification Quality Checklist.
- 📁 Files: `specs/050-crm-db-foundations/spec.md`, `specs/050-crm-db-foundations/checklists/requirements.md`
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The existing feature branch and directory structure were already in place, so the focus was on updating the specification to perfectly align with the template and the user's detailed prompt while maintaining a "WHAT" and "WHY" focus.

## Evaluation notes (flywheel)

- Failure modes observed: PHR script returned empty output on Windows/PowerShell.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Fix PHR script for Windows environment.
