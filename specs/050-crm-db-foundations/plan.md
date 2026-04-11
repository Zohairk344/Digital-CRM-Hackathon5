# Implementation Plan: CRM Database Foundations

**Branch**: `050-crm-db-foundations` | **Date**: 2026-03-24 | **Spec**: [specs/050-crm-db-foundations/spec.md](spec.md)
**Input**: Build the foundational Database configuration and SQLAlchemy ORM models for the CRM Digital FTE Factory.

## Summary

This feature establishes the core data persistence layer for the CRM. It involves setting up an asynchronous PostgreSQL connection using SQLAlchemy 2.0 and `asyncpg`, configuring environment-based settings with Pydantic, and defining the primary ORM models: `Customer`, `Ticket`, `Message`, and `KnowledgeArticle` (with `pgvector` support).

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.0 (Async), asyncpg, pydantic-settings, pgvector  
**Storage**: PostgreSQL 16+ with pgvector extension  
**Testing**: pytest with pytest-asyncio  
**Target Platform**: Linux/Docker  
**Project Type**: Web Backend (FastAPI)  

## Constitution Check

- [x] Backend uses Python 3.12+, FastAPI, SQLAlchemy (Async), Pydantic v2.
- [x] Use `uv` for all operations.
- [x] PostgreSQL with pgvector is specified for state management.
- [x] Type safety with Pydantic and Python type hints.
- [x] Monorepo structure (/backend) is maintained.

## 1. File Tree Changes

| Path | Action | Description |
|------|--------|-------------|
| `backend/app/core/config.py` | Create/Modify | Pydantic `BaseSettings` for DB configuration. |
| `backend/app/db/database.py` | Create/Modify | SQLAlchemy `AsyncEngine` and `async_sessionmaker`. |
| `backend/app/db/models.py` | Create/Modify | Declarative base and SQLAlchemy ORM models. |
| `backend/.env` | Create/Modify | Local environment variables for DB credentials. |
| `backend/tests/test_db.py` | Create/Modify | Integration tests for DB connection and models. |

## 2. Dependency Management

Run the following command to ensure all necessary libraries are installed:
```bash
cd backend
uv add fastapi sqlalchemy asyncpg pydantic-settings pgvector pytest pytest-asyncio
```

## 3. Step-by-Step Implementation Logic

### Phase A: Configuration & Environment
- **File**: `backend/app/core/config.py`
- **Logic**: 
  - Define `Settings` class inheriting from Pydantic `BaseSettings`.
  - Include fields for `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SERVER`, `POSTGRES_PORT`, `POSTGRES_DB`.
  - Add a property `SQLALCHEMY_DATABASE_URI` that constructs the async connection string: `postgresql+asyncpg://{USER}:{PASS}@{SERVER}:{PORT}/{DB}`.
  - Load from `.env` file using `model_config = SettingsConfigDict(env_file=".env")`.

### Phase B: Database Connection
- **File**: `backend/app/db/database.py`
- **Logic**:
  - Import `create_async_engine` and `async_sessionmaker` from `sqlalchemy.ext.asyncio`.
  - Initialize `engine` using the URI from `config`.
  - **Safety**: Set `pool_pre_ping=True` to handle connection drops gracefully.
  - Create `AsyncSessionLocal` using `async_sessionmaker(bind=engine, expire_on_commit=False)`.
  - Provide a `get_db` dependency for FastAPI.

### Phase C: Base Model & Extensions
- **File**: `backend/app/db/models.py`
- **Logic**:
  - Create a `Base` class using `DeclarativeBase`.
  - Note: Ensure the `pgvector` extension is handled (usually requires `CREATE EXTENSION IF NOT EXISTS vector;` in migrations or a separate init script).

### Phase D: ORM Models
- **File**: `backend/app/db/models.py`
- **Logic**:
  - **Customer**: UUID PK, Unique Email/Phone (nullable), `is_active`, `deleted_at`, relationships to Tickets. Enforce `CheckConstraint` for Email OR Phone.
  - **Ticket**: UUID PK, FK to Customer, Status/Priority/Channel Enums, `is_active`, `deleted_at`, `metadata` (JSONB).
  - **Message**: UUID PK, FK to Ticket, Nullable `agent_id`, Sender Type/Channel Enums, Content, Sentiment Score, `is_active`, `deleted_at`, `metadata` (JSONB).
  - **KnowledgeArticle**: UUID PK, Title, Content, `Vector(1536)` embedding, `embedding_model` string.
  - **OutboxEvent**: UUID PK, Payload (JSONB), Event Type, Status, Created At (for Kafka atomicity).
  - **Relationships**: Use `relationship()` with `back_populates` for all links.

## 4. Validation Strategy

- **Integration Test**: Create `backend/tests/test_db.py` that:
  - Connects to a test database.
  - Emits `Base.metadata.create_all()` via an async wrapper.
  - Inserts a dummy `Customer`, `Ticket`, and `Message` to verify relationships and constraints.
  - Performs a simple vector similarity query on `KnowledgeArticle` to verify `pgvector` support.
- **Environment Check**: Verify `.env` variables are correctly loaded into `config.py`.

## Project Structure (Documentation)

```text
specs/050-crm-db-foundations/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── database-ops.yaml
```
