# Quickstart: CRM Database Foundations

## Environment Setup

1. **Install dependencies**:
   ```bash
   cd backend
   uv add fastapi sqlalchemy asyncpg pydantic-settings pgvector pytest pytest-asyncio
   ```

2. **Configure environment**:
   Create `backend/.env` with the following:
   ```env
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=crm_db
   ```

3. **Initialize Database**:
   - Ensure PostgreSQL 16+ is running.
   - Run `CREATE EXTENSION IF NOT EXISTS vector;` in your DB console.

## Initial Verification

Run the following command to verify the model definitions and connection:
```bash
cd backend
uv run pytest tests/test_db.py
```

## Core Files Created

- `app/core/config.py`: Loads environment variables via Pydantic.
- `app/db/database.py`: Manages the async database engine and sessions.
- `app/db/models.py`: Defines the SQLAlchemy ORM models.
