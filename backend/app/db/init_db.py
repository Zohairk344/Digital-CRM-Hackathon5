import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("POSTGRES_USER", "user")
os.environ.setdefault("POSTGRES_PASSWORD", "password")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "crm_db")
os.environ.setdefault("KAFKA_BROKER_URL", "localhost:9092")
os.environ.setdefault("KAFKA_TOPIC_SUPPORT_TICKETS", "support.tickets.new")

from sqlalchemy import text
from app.db.database import engine
from app.db.models import Base

async def init_db():
    async with engine.begin() as conn:
        print("Checking for pgvector extension...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        
    print("Database initialization complete.")

if __name__ == "__main__":
    asyncio.run(init_db())