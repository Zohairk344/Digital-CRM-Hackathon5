import pytest
import asyncio
import json
import signal
from unittest.mock import AsyncMock, patch, MagicMock
from app.workers.main_worker import main

@pytest.mark.asyncio
async def test_worker_processes_message(caplog):
    # Mock message
    mock_payload = {
        "ticket_id": "123-abc",
        "subject": "Test Issue",
        "description": "I need help",
        "metadata": {},
        "status": "new",
        "timestamp": "2026-04-04T12:00:00Z"
    }
    
    # Create a mock for the message object returned by getmany
    mock_msg = MagicMock()
    mock_msg.value = mock_payload
    
    # Create a mock consumer
    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.start = AsyncMock()
    mock_consumer_instance.stop = AsyncMock()
    
    # Define a sequence for getmany to avoid infinite loop
    # Return one message then an empty dict to stop the loop (with help of shutdown_event)
    mock_consumer_instance.getmany.side_effect = [
        {MagicMock(): [mock_msg]},
        {}
    ]

    with patch("app.workers.main_worker.AIOKafkaConsumer", return_value=mock_consumer_instance):
        # We need a way to stop the main loop. 
        # I'll patch asyncio.Event so I can set it after one call.
        with patch("asyncio.Event") as mock_event_class:
            mock_event_instance = mock_event_class.return_value
            # We want is_set() to return True after the first call to getmany
            mock_event_instance.is_set.side_effect = [False, True]
            
            await main()
        
    # Verify logging
    ticket_record = next((r for r in caplog.records if r.message == "Support Ticket Received"), None)
    assert ticket_record is not None
    assert ticket_record.ticket_id == "123-abc"
    assert "Worker stopped gracefully" in caplog.text

@pytest.mark.asyncio
async def test_worker_shutdown_on_signal(caplog):
    # Create a mock consumer
    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.getmany.return_value = {}

    with patch("app.workers.main_worker.AIOKafkaConsumer", return_value=mock_consumer_instance):
        # We want to simulate a signal setting the event
        with patch("asyncio.Event") as mock_event_class:
            mock_event_instance = mock_event_class.return_value
            # Simulate event being set after first check
            mock_event_instance.is_set.side_effect = [False, True]
            
            await main()
            
    assert "Stopping consumer and committing offsets..." in caplog.text
    assert "Worker stopped gracefully" in caplog.text
