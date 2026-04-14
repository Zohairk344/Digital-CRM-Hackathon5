from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
import logging

from app.db.models import Customer, Ticket, Message, KnowledgeArticle, OutboxEvent

logger = logging.getLogger(__name__)

# --- Customer CRUD ---

async def create_customer(
    db: AsyncSession, 
    email: Optional[str] = None, 
    phone: Optional[str] = None,
    commit: bool = True
) -> Customer:
    """
    Creates a new customer record.
    Constraints ensure either email or phone is present.
    """
    db_customer = Customer(email=email, phone=phone)
    db.add(db_customer)
    if commit:
        await db.commit()
        await db.refresh(db_customer)
    return db_customer

async def get_customer_by_email(db: AsyncSession, email: str) -> Optional[Customer]:
    """
    Retrieves a customer by email.
    """
    result = await db.execute(select(Customer).filter(Customer.email == email, Customer.is_active == True))
    return result.scalars().first()

async def get_customer_by_phone(db: AsyncSession, phone: str) -> Optional[Customer]:
    """
    Retrieves a customer by phone number.
    """
    result = await db.execute(select(Customer).filter(Customer.phone == phone, Customer.is_active == True))
    return result.scalars().first()


async def get_or_create_customer(
    db: AsyncSession,
    email: Optional[str] = None,
    phone: Optional[str] = None
) -> Customer:
    """
    Atomically get or create a customer using PostgreSQL UPSERT.
    Uses INSERT ... ON CONFLICT DO NOTHING to avoid race conditions.
    """
    # First try to find existing customer
    if email:
        existing = await get_customer_by_email(db, email)
        if existing:
            return existing
    if phone:
        existing = await get_customer_by_phone(db, phone)
        if existing:
            return existing
    
    # Try to insert - use upsert to handle concurrent inserts safely
    if email:
        stmt = insert(Customer).values(email=email, phone=phone).on_conflict_do_nothing(
            index_elements=['email']
        ).returning(Customer)
    elif phone:
        stmt = insert(Customer).values(email=email, phone=phone).on_conflict_do_nothing(
            index_elements=['phone']
        ).returning(Customer)
    else:
        raise ValueError("At least one of email or phone must be provided")
    
    result = await db.execute(stmt)
    customer = result.scalars().first()
    
    if customer is None:
        # Conflict occurred - fetch existing customer
        if email:
            existing = await get_customer_by_email(db, email)
            if existing:
                return existing
        if phone:
            existing = await get_customer_by_phone(db, phone)
            if existing:
                return existing
    
    return customer

# --- Ticket CRUD ---

async def create_ticket(
    db: AsyncSession,
    customer_id: Any,
    channel_origin: str,
    status: str = "open",
    priority: str = "medium",
    metadata_json: Optional[dict[str, Any]] = None,
    commit: bool = True
) -> Ticket:
    """
    Creates a new support ticket.
    """
    db_ticket = Ticket(
        customer_id=customer_id,
        channel_origin=channel_origin,
        status=status,
        priority=priority,
        metadata_json=metadata_json
    )
    db.add(db_ticket)
    if commit:
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket

async def get_ticket(db: AsyncSession, ticket_id: Any) -> Optional[Ticket]:
    """
    Retrieves a ticket by ID.
    """
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id, Ticket.is_active == True))
    return result.scalars().first()

# --- Message CRUD ---

async def create_message(
    db: AsyncSession,
    ticket_id: Any,
    sender_type: str,
    channel: str,
    content: str,
    agent_id: Optional[Any] = None,
    sentiment_score: Optional[float] = None,
    metadata_json: Optional[dict[str, Any]] = None,
    commit: bool = True
) -> Message:
    """
    Creates a new message within a ticket.
    """
    db_message = Message(
        ticket_id=ticket_id,
        sender_type=sender_type,
        channel=channel,
        content=content,
        agent_id=agent_id,
        sentiment_score=sentiment_score,
        metadata_json=metadata_json
    )
    db.add(db_message)
    if commit:
        await db.commit()
        await db.refresh(db_message)
    return db_message

async def get_ticket_messages(db: AsyncSession, ticket_id: Any) -> List[Message]:
    """
    Retrieves all active messages for a ticket in chronological order.
    """
    result = await db.execute(
        select(Message)
        .filter(Message.ticket_id == ticket_id, Message.is_active == True)
        .order_by(Message.created_at.asc())
    )
    return list(result.scalars().all())

# --- KnowledgeArticle CRUD ---

async def create_knowledge_article(
    db: AsyncSession,
    title: str,
    content: str,
    embedding: List[float],
    embedding_model: str,
    commit: bool = True
) -> KnowledgeArticle:
    """
    Creates a new knowledge article.
    """
    db_article = KnowledgeArticle(
        title=title,
        content=content,
        embedding=embedding,
        embedding_model=embedding_model
    )
    db.add(db_article)
    if commit:
        await db.commit()
        await db.refresh(db_article)
    return db_article

async def search_knowledge_base(
    db: AsyncSession,
    query_embedding: List[float],
    limit: int = 5
) -> List[KnowledgeArticle]:
    """
    Performs semantic search on knowledge articles using vector similarity.
    """
    result = await db.execute(
        select(KnowledgeArticle)
        .order_by(KnowledgeArticle.embedding.l2_distance(query_embedding))
        .limit(limit)
    )
    return list(result.scalars().all())

# --- Outbox CRUD ---

async def create_outbox_event(
    db: AsyncSession,
    event_type: str,
    payload: dict[str, Any],
    commit: bool = True
) -> OutboxEvent:
    """
    Creates a new outbox event for Kafka.
    """
    db_event = OutboxEvent(event_type=event_type, payload=payload)
    db.add(db_event)
    if commit:
        await db.commit()
        await db.refresh(db_event)
    return db_event
