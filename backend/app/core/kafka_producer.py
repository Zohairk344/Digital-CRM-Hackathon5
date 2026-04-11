import json
import logging
from typing import Any, Optional
from aiokafka import AIOKafkaProducer
from app.core.config import settings

logger = logging.getLogger(__name__)

class KafkaProducer:
    """
    A wrapper around AIOKafkaProducer for asynchronous message publishing.
    """
    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self.broker_url = settings.KAFKA_BROKER_URL

    async def start(self):
        """
        Starts the Kafka producer.
        """
        if self._producer is not None:
            return

        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.broker_url,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            await self._producer.start()
            logger.info(f"Kafka producer started and connected to {self.broker_url}")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            self._producer = None
            # Per instructions: log the error but do not crash the application.

    async def stop(self):
        """
        Stops the Kafka producer.
        """
        if self._producer:
            await self._producer.stop()
            self._producer = None
            logger.info("Kafka producer stopped")

    async def send_message(self, topic: str, payload: Any):
        """
        Sends a message to a specific Kafka topic.
        """
        if self._producer is None:
            logger.warning("Kafka producer not started. Message not sent.")
            raise ConnectionError("Kafka producer not started")

        try:
            await self._producer.send_and_wait(topic, payload)
            logger.debug(f"Message sent to topic {topic}")
        except Exception as e:
            logger.error(f"Error sending message to Kafka topic {topic}: {e}")
            raise e

# Global instance
kafka_producer = KafkaProducer()
