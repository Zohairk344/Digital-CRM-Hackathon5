# AGENTS.md - Hackathon5

## Project Structure
- `frontend/` - Next.js 16 (App Router), React 19, Tailwind CSS 4
- `backend/` - Python 3.13+, FastAPI, SQLAlchemy, async Kafka (aiokafka)
- `specs/` - Feature specifications (each has `spec.md`, `plan.md`, `tasks.md`)
- `docker-compose.yml` - PostgreSQL (pgvector), Redpanda (Kafka), Console

## Running the Project

```bash
# Start infrastructure
docker-compose up -d

# Frontend (Next.js 16)
cd frontend && npm run dev

# Backend (FastAPI with uv)
cd backend && uv run fastapi dev
```

## Commands

```bash
# Frontend
cd frontend && npm run build    # Production build
cd frontend && npm run lint     # ESLint

# Backend (uses uv)
cd backend && uv run pytest           # All tests
cd backend && uv run pytest tests/   # Specific test dir
```

## Key Notes

- **Next.js 16** has breaking changes from older versions. Check `node_modules/next/dist/docs/` before writing code.
- **Python** requires uv. Use `uv run` instead of `python` for commands.
- **Database** runs on port 5432 (pgvector/pg16). Kafka on 9092, Console on 8080.
- **Spec workflow** uses `.gemini/commands/` - see `GEMINI.md` for details.
- Backend uses Pydantic v2 and pytest-asyncio with `asyncio_mode = "auto"`.