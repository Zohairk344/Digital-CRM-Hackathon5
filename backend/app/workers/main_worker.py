import asyncio
import logging
import os
import json
import signal
import uuid
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from pythonjsonlogger import jsonlogger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

# App Imports
from app.ai.agent import process_ticket
from app.db.database import AsyncSessionLocal
from app.db.models import Ticket, Message

# Configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "support.tickets.new")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "fte-ai-worker-group")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def setup_logging():
    """Setup structured JSON logging."""
    logger = logging.getLogger()
    if not logger.handlers:
        log_handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
    logger.setLevel(LOG_LEVEL)
    return logger

logger = setup_logging()

async def main():
    """Main worker entrypoint."""
    logger.info("Starting Kafka Consumer Worker", extra={
        "broker_url": KAFKA_BROKER_URL,
        "topic": KAFKA_TOPIC,
        "group_id": KAFKA_GROUP_ID
    })

    # Shutdown event
    shutdown_event = asyncio.Event()

    def handle_signal():
        logger.info("Received shutdown signal")
        shutdown_event.set()

    # Bind signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, handle_signal)
        except NotImplementedError:
            pass

    # Initialize AIOKafkaConsumer
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    # Start the consumer with retry logic
    while True:
        try:
            await consumer.start()
            logger.info("Consumer started and subscribed to topic", extra={"topic": KAFKA_TOPIC})
            break
        except KafkaConnectionError:
            logger.warning("Kafka broker unavailable, retrying in 5 seconds...", extra={
                "broker_url": KAFKA_BROKER_URL
            })
            await asyncio.sleep(5)

    try:
        # Polling loop with shutdown check
        while not shutdown_event.is_set():
            try:
                result = await consumer.getmany(timeout_ms=1000)
                for tp, messages in result.items():
                    for msg in messages:
                        payload = msg.value
                        ticket_id_str = payload.get("ticket_id")
                        
                        if not ticket_id_str:
                            logger.error("Malformed Kafka message: missing ticket_id", extra={"payload": payload})
                            continue

                        # --- Integration Loop with Global Try/Except ---
                        try:
                            # 1. AI Invocation
                            # We provide the payload which should contain subject/description
                            # If not, the process_ticket helper handles defaults
                            ai_result = await process_ticket(payload)

                            # 2. Database Transaction
                            async with AsyncSessionLocal() as session:
                                ticket_uuid = uuid.UUID(ticket_id_str)
                                # Fetch the Ticket
                                ticket = await session.get(Ticket, ticket_uuid)
                                
                                if ticket:
                                    # Update attributes as per requirements
                                    ticket.category = ai_result.category.value
                                    ticket.sentiment = ai_result.sentiment_label.value
                                    ticket.suggested_response = ai_result.suggested_response
                                    ticket.is_escalated = ai_result.is_escalated
                                    ticket.status = "AI_PROCESSED"
                                    
                                    await session.commit()
                                    logger.info("Ticket processed and database updated successfully", extra={
                                        "ticket_id": ticket_id_str,
                                        "category": ticket.category,
                                        "sentiment": ticket.sentiment
                                    })
                                else:
                                    logger.warning("Ticket not found in database", extra={"ticket_id": ticket_id_str})

                        except Exception as e:
                            logger.error("Failed to process ticket", extra={
                                "ticket_id": ticket_id_str,
                                "error": str(e)
                            })
                            continue # Ensure the loop survives

            except Exception as e:
                logger.error("Error in polling loop", extra={"error": str(e)})
                await asyncio.sleep(1)
    finally:
        logger.info("Stopping consumer...")
        await consumer.stop()
        logger.info("Worker stopped gracefully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, exiting...")
