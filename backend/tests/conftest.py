import asyncio
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.database import engine as main_engine
from app.db.models import Base

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an async database session that rolls back after each test.
    This ensures test isolation.
    """
    # Create tables
    async with main_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Connect and start transaction
    connection = await main_engine.connect()
    transaction = await connection.begin()
    
    async_session = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    
    session = async_session()
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()
    
    # Optional: clean up tables
    # async with main_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
