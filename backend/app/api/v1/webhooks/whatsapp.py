from typing import List
import re
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.database import get_db
from app.db import crud
from app.core.sentiment import get_sentiment_score

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


class WhatsAppPayload(BaseModel):
    phone_number: str
    message: str
    name: str


def sanitize_phone_number(phone: str) -> str:
    """
    Sanitize phone number by removing non-digit characters.
    Example: "+1-234-567-8900" -> "1234567890"
    """
    return re.sub(r'\D', '', phone)


@router.get("/whatsapp/health")
async def health_check():
    return {"status": "ok", "channel": "whatsapp"}


@router.post("/whatsapp", status_code=status.HTTP_201_CREATED)
async def receive_whatsapp_webhook(
    payload: WhatsAppPayload,
    db: AsyncSession = Depends(get_db)
):
    try:
        async with db.begin():
            # 1. Sanitize phone number
            sanitized_phone = sanitize_phone_number(payload.phone_number)

            # 2. Sentiment Analysis
            sentiment_score = get_sentiment_score(payload.message)

            # 3. Escalation Logic (same as web_form)
            priority = "medium"
            tags: List[str] = []

            # Pricing/Competitor keywords
            pricing_keywords = ["pricing", "cost", "quote", "discount", "competitor"]
            if any(kw in payload.message.lower() for kw in pricing_keywords):
                priority = "urgent"
                tags.append("pricing_escalation")

            # Negative Sentiment
            if sentiment_score < 0.3:
                priority = "urgent"
                tags.append("negative_sentiment")

            # 4. Customer lookup/creation
            customer = await crud.get_customer_by_phone(db, sanitized_phone)
            if not customer:
                customer = await crud.create_customer(
                    db,
                    email=None,
                    phone=sanitized_phone,
                    commit=False
                )
                await db.flush()

            # 5. Ticket creation
            ticket_metadata = {
                "whatsapp_sender_name": payload.name,
                "subject": f"WhatsApp Message from {payload.name}",
                "tags": tags
            }

            ticket = await crud.create_ticket(
                db,
                customer_id=customer.id,
                channel_origin="WHATSAPP",
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
                channel="whatsapp",
                content=payload.message,
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
                    "channel": "whatsapp",
                    "priority": priority,
                    "sentiment_score": sentiment_score
                },
                commit=False
            )

            await db.flush()

            return {
                "status": "success",
                "ticket_id": str(ticket.id),
                "channel": "whatsapp"
            }

    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )