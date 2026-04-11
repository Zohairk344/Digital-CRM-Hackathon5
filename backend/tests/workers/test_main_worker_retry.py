import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from aiokafka.errors import KafkaConnectionError
from app.workers.main_worker import main

@pytest.mark.asyncio
async def test_worker_retries_on_connection_error(caplog):
    # Create a mock consumer
    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.start = AsyncMock()
    mock_consumer_instance.stop = AsyncMock()
    
    # Simulate KafkaConnectionError once, then success
    mock_consumer_instance.start.side_effect = [KafkaConnectionError("Broker unavailable"), None]
    
    # Mock getmany to return empty results and stop immediately via shutdown event
    mock_consumer_instance.getmany.return_value = {}

    with patch("app.workers.main_worker.AIOKafkaConsumer", return_value=mock_consumer_instance):
        with patch("asyncio.Event") as mock_event_class:
            mock_event_instance = mock_event_class.return_value
            # Check is_set: False (to enter loop), True (to exit loop after one check)
            mock_event_instance.is_set.side_effect = [False, True]
            
            # We also need to speed up the sleep in main_worker
            with patch("asyncio.sleep", return_value=None) as mock_sleep:
                await main()
                
                # Verify sleep was called once with 5 seconds
                mock_sleep.assert_any_call(5)
        
    # Verify logging of the warning
    assert "Kafka broker unavailable, retrying in 5 seconds..." in caplog.text
    assert "Consumer started and subscribed to topic" in caplog.text
