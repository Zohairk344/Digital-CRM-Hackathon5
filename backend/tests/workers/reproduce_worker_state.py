import asyncio
import json
import os
import uuid
from aiokafka import AIOKafkaProducer

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "support.tickets.new")

async def send_test_ticket():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        ticket_id = str(uuid.uuid4())
        payload = {
            "ticket_id": ticket_id,
            "subject": "Test Ticket",
            "description": "This is a test ticket for integration."
        }
        print(f"Sending test ticket: {ticket_id}")
        await producer.send_and_wait(KAFKA_TOPIC, payload)
        print("Message sent successfully")
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(send_test_ticket())
