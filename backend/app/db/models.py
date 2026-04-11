from datetime import datetime, timezone
import uuid
from typing import Optional, List, Any
from sqlalchemy import Column, DateTime, MetaData, String, CheckConstraint, UniqueConstraint, Enum, ForeignKey, Text, Float, Index, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

# Define naming convention for constraints to help with migrations
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    Uses the modern SQLAlchemy 2.0 DeclarativeBase style.
    """
    metadata = metadata

class TimestampMixin:
    """
    A mixin to add created_at and updated_at columns to models.
    All timestamps are stored in UTC.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class IDMixin:
    """
    A mixin to add a UUID primary key to models.
    """
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

class SoftDeleteMixin:
    """
    A mixin to add soft deletion functionality.
    """
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class Customer(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Customer model for multi-channel identification.
    Requires at least an email or a phone number.
    """
    __tablename__ = "customer"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL) OR (phone IS NOT NULL)",
            name="ck_customer_contact_info_present"
        ),
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, email={self.email}, phone={self.phone})>"

    # Relationships
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

class Ticket(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Ticket model to track support requests.
    """
    __tablename__ = "ticket"

    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True) # open, AI_PROCESSED, in_progress, resolved, escalated
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False, index=True) # low, medium, high
    channel_origin: Mapped[str] = mapped_column(String(20), nullable=False, index=True) # web, gmail, whatsapp
    
    # AI Analysis Fields
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sentiment_label: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_escalated: Mapped[bool] = mapped_column(default=False, nullable=False)
    suggested_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("idx_ticket_customer_created", "customer_id", Column("created_at").desc()),
    )

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    messages: Mapped[List["Message"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, customer_id={self.customer_id}, status={self.status})>"

class Message(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Message model for interactions within a ticket.
    """
    __tablename__ = "message"

    ticket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ticket.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True) # customer, agent
    channel: Mapped[str] = mapped_column(String(20), nullable=False, index=True) # web, gmail, whatsapp
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("idx_message_ticket_created", "ticket_id", Column("created_at").desc()),
    )

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, ticket_id={self.ticket_id}, sender_type={self.sender_type})>"

class OutboxEvent(Base, IDMixin, TimestampMixin):
    """
    OutboxEvent model for Kafka event atomicity.
    """
    __tablename__ = "outbox_event"

    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True) # pending, processed, failed
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<OutboxEvent(id={self.id}, event_type={self.event_type}, status={self.status})>"

class KnowledgeArticle(Base, IDMixin, TimestampMixin):
    """
    KnowledgeArticle model for semantic search.
    """
    __tablename__ = "knowledge_article"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., 'text-embedding-3-small'

    def __repr__(self) -> str:
        return f"<KnowledgeArticle(id={self.id}, title={self.title})>"
