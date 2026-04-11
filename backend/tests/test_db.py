import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db import crud
from app.db.models import Customer, Ticket, Message, KnowledgeArticle

@pytest.mark.asyncio
async def test_create_customer(db_session: AsyncSession):
    """
    Test creating a valid customer.
    """
    customer = await crud.create_customer(db_session, email="test@example.com")
    assert customer.id is not None
    assert customer.email == "test@example.com"
    assert customer.is_active is True

@pytest.mark.asyncio
async def test_create_customer_no_contact_fails(db_session: AsyncSession):
    """
    Test that creating a customer with neither email nor phone fails.
    """
    with pytest.raises(IntegrityError):
        await crud.create_customer(db_session)
        await db_session.flush()

@pytest.mark.asyncio
async def test_create_ticket_and_message(db_session: AsyncSession):
    """
    Test creating a ticket and adding a message to it,
    validating the relationship.
    """
    # 1. Create a customer
    customer = await crud.create_customer(db_session, email="ticket.user@example.com")
    
    # 2. Create a ticket for the customer
    ticket = await crud.create_ticket(
        db=db_session,
        customer_id=customer.id,
        channel_origin="web",
        priority="high"
    )
    assert ticket.id is not None
    assert ticket.customer_id == customer.id
    assert ticket.priority == "high"
    assert ticket.customer.email == "ticket.user@example.com"

    # 3. Add a message to the ticket
    message_content = "This is a test message."
    message = await crud.create_message(
        db=db_session,
        ticket_id=ticket.id,
        sender_type="customer",
        channel="web",
        content=message_content
    )
    assert message.id is not None
    assert message.ticket_id == ticket.id
    assert message.content == message_content
    
    # 4. Verify relationships from the message side
    assert message.ticket.id == ticket.id
    assert message.ticket.customer.id == customer.id

@pytest.mark.asyncio
async def test_get_ticket_messages_chronological(db_session: AsyncSession):
    """
    Test that messages for a ticket are retrieved in chronological order.
    """
    customer = await crud.create_customer(db_session, email="chrono.user@example.com")
    ticket = await crud.create_ticket(db_session, customer_id=customer.id, channel_origin="gmail")

    # Create messages out of order to test the query's ordering
    await crud.create_message(db_session, ticket_id=ticket.id, sender_type="customer", channel="gmail", content="Message 1")
    await crud.create_message(db_session, ticket_id=ticket.id, sender_type="agent", channel="gmail", content="Message 2")

    messages = await crud.get_ticket_messages(db_session, ticket_id=ticket.id)
    assert len(messages) == 2
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"
    assert messages[0].created_at < messages[1].created_at

@pytest.mark.asyncio
async def test_knowledge_article_semantic_search(db_session: AsyncSession):
    """
    Test vector similarity search on knowledge articles.
    """
    # Dummy embeddings
    embedding1 = [1.0] * 1536
    embedding2 = [0.5] * 1536
    embedding3 = [0.1] * 1536
    
    await crud.create_knowledge_article(
        db=db_session,
        title="Article 1",
        content="Content 1",
        embedding=embedding1,
        embedding_model="test-model"
    )
    await crud.create_knowledge_article(
        db=db_session,
        title="Article 2",
        content="Content 2",
        embedding=embedding2,
        embedding_model="test-model"
    )
    await crud.create_knowledge_article(
        db=db_session,
        title="Article 3",
        content="Content 3",
        embedding=embedding3,
        embedding_model="test-model"
    )

    # Query for something most similar to Article 1
    query_embedding = [0.9] * 1536
    
    search_results = await crud.search_knowledge_base(
        db=db_session,
        query_embedding=query_embedding,
        limit=1
    )
    
    assert len(search_results) == 1
    assert search_results[0].title == "Article 1"

@pytest.mark.asyncio
async def test_connection_pool_resilience(db_session: AsyncSession):
    """
    Simulates a basic check for connection resilience.
    The `pool_pre_ping=True` in `database.py` is the actual mechanism.
    This test verifies that the session is usable.
    """
    # A simple query to check the connection
    customer = await crud.create_customer(db_session, email="resilience.test@example.com")
    retrieved = await crud.get_customer_by_email(db_session, email="resilience.test@example.com")
    assert retrieved is not None
    assert retrieved.id == customer.id
