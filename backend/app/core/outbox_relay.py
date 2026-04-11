import asyncio
import logging
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.models import OutboxEvent
from app.core.kafka_producer import kafka_producer
from app.core.config import settings

logger = logging.getLogger(__name__)

async def run_outbox_relay():
    """
    Background task that polls the OutboxEvent table and publishes pending events to Kafka.
    """
    logger.info("Outbox relay background task starting...")
    
    backoff = 5
    max_backoff = 60
    
    while True:
        try:
            # Check if producer is ready
            if not kafka_producer._producer:
                logger.warning("Kafka producer not ready, attempting to restart...")
                await kafka_producer.start()
            
            processed_count = await process_outbox_events()
            
            if processed_count > 0:
                # Reset backoff on success
                backoff = 5
            else:
                # No events to process, standard sleep
                backoff = 5
                
        except Exception as e:
            logger.error(f"Error in outbox relay loop: {e}")
            # Exponential backoff on loop failure (e.g., DB down, Kafka down)
            backoff = min(backoff * 2, max_backoff)
            logger.info(f"Retrying outbox relay in {backoff} seconds...")
        
        # Non-blocking sleep to yield control back to the event loop
        await asyncio.sleep(backoff)

async def process_outbox_events() -> int:
    """
    Fetches pending outbox events and attempts to publish them.
    Returns the number of events attempted.
    """
    async with AsyncSessionLocal() as session:
        # Fetch pending events, ordered by creation time (FIFO), limited to 50
        stmt = (
            select(OutboxEvent)
            .where(OutboxEvent.status == "pending")
            .order_by(OutboxEvent.created_at.asc())
            .limit(50)
        )
        result = await session.execute(stmt)
        events = result.scalars().all()

        if not events:
            return 0

        logger.info(f"Fetched {len(events)} pending outbox events.")

        processed_count = 0
        for event in events:
            try:
                # Attempt to publish the event to Kafka
                topic = settings.KAFKA_TOPIC_SUPPORT_TICKETS
                await kafka_producer.send_message(topic, event.payload)
                
                # Mark as processed upon successful publish
                event.status = "processed"
                logger.info(f"Successfully published outbox event {event.id} to {topic}")
            except Exception as e:
                # Increment retry count on failure
                event.retry_count += 1
                logger.error(f"Failed to publish outbox event {event.id}: {e}")
                
                # Mark as failed if retry limit reached (US2)
                if event.retry_count >= 3:
                    event.status = "failed"
                    logger.warning(f"Event {event.id} reached maximum retries and is marked as 'failed'.")
            
            # Commit after each event for atomicity (At-least-once)
            await session.commit()
            processed_count += 1
            
        return processed_count
