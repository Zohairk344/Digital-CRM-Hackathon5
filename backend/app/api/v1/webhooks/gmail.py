from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.database import get_db
from app.db import crud
from app.core.sentiment import get_sentiment_score

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


class GmailPayload(BaseModel):
    sender_email: EmailStr
    subject: str
    body: str


@router.get("/gmail/health")
async def health_check():
    return {"status": "ok", "channel": "gmail"}


@router.post("/gmail", status_code=status.HTTP_201_CREATED)
async def receive_gmail_webhook(
    payload: GmailPayload,
    db: AsyncSession = Depends(get_db)
):
    try:
        async with db.begin():
            # 1. Normalize email (lowercase)
            normalized_email = payload.sender_email.lower()

            # 2. Sentiment Analysis
            sentiment_score = get_sentiment_score(payload.body)

            # 3. Escalation Logic (same as web_form)
            priority = "medium"
            tags: List[str] = []

            # Pricing/Competitor keywords
            pricing_keywords = ["pricing", "cost", "quote", "discount", "competitor"]
            if any(kw in payload.body.lower() for kw in pricing_keywords):
                priority = "urgent"
                tags.append("pricing_escalation")

            # Negative Sentiment
            if sentiment_score < 0.3:
                priority = "urgent"
                tags.append("negative_sentiment")

            # 4. Customer lookup/creation (thread-safe)
            customer = await crud.get_or_create_customer(
                db,
                email=normalized_email
            )

            # 5. Ticket creation
            ticket_metadata = {
                "gmail_subject": payload.subject,
                "tags": tags
            }

            ticket = await crud.create_ticket(
                db,
                customer_id=customer.id,
                channel_origin="GMAIL",
                priority=priority,
                metadata_json=ticket_metadata,
                commit=False
            )
            await db.flush()

            # 6. Message creation
            await crud.create_message(
                db,
                ticket_id=ticket.id,
                sender_type="customer",
                channel="gmail",
                content=payload.body,
                sentiment_score=sentiment_score,
                commit=False
            )

            # 7. Outbox Event for Kafka
            await crud.create_outbox_event(
                db,
                event_type="ticket.created",
                payload={
                    "ticket_id": str(ticket.id),
                    "customer_id": str(customer.id),
                    "channel": "gmail",
                    "priority": priority,
                    "sentiment_score": sentiment_score
                },
                commit=False
            )

            await db.flush()

            return {
                "status": "success",
                "ticket_id": str(ticket.id),
                "channel": "gmail"
            }

    except Exception as e:
        logger.error(f"Error processing Gmail webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )