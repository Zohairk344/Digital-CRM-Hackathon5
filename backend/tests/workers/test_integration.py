import pytest
import asyncio
import uuid
from unittest.mock import AsyncMock, patch, MagicMock
from app.workers.main_worker import process_message
from app.ai.agent import AIAgent, TicketAnalysis, CategoryEnum, SentimentLabelEnum

@pytest.mark.asyncio
async def test_process_message_success(caplog):
    # Mock data
    ticket_id = str(uuid.uuid4())
    payload = {
        "ticket_id": ticket_id,
        "subject": "Login Problem"
    }
    
    # Mock AI Agent
    mock_agent = MagicMock(spec=AIAgent)
    mock_analysis = TicketAnalysis(
        category=CategoryEnum.TECHNICAL,
        sentiment_label=SentimentLabelEnum.NEGATIVE,
        sentiment_score=0.2,
        is_escalated=True,
        suggested_response="* Try resetting your password."
    )
    mock_agent.process_ticket = AsyncMock(return_value=mock_analysis)
    
    # Mock DB Ticket
    mock_ticket = MagicMock()
    mock_ticket.id = uuid.UUID(ticket_id)
    
    # Mock DB Message
    mock_message = MagicMock()
    mock_message.content = "I cannot log in to my account."
    
    # Mock Database Session
    mock_session = AsyncMock()
    mock_result_ticket = MagicMock()
    mock_result_ticket.scalars().first.return_value = mock_ticket
    
    mock_result_msg = MagicMock()
    mock_result_msg.scalars().all.return_value = [mock_message]
    
    mock_session.execute.side_effect = [mock_result_ticket, mock_result_msg]
    
    # Mock AsyncSessionLocal context manager
    with patch("app.workers.main_worker.AsyncSessionLocal", return_value=MagicMock(__aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock())):
        await process_message(payload, mock_agent)
    
    # Assertions
    assert mock_ticket.category == CategoryEnum.TECHNICAL
    assert mock_ticket.sentiment_label == SentimentLabelEnum.NEGATIVE
    assert mock_ticket.sentiment_score == 0.2
    assert mock_ticket.is_escalated is True
    assert mock_ticket.suggested_response == "* Try resetting your password."
    assert mock_ticket.status == "AI_PROCESSED"
    
    mock_session.commit.assert_awaited_once()
    assert "Ticket successfully enriched by AI" in caplog.text

@pytest.mark.asyncio
async def test_process_message_ticket_not_found(caplog):
    ticket_id = str(uuid.uuid4())
    payload = {"ticket_id": ticket_id}
    
    mock_agent = MagicMock(spec=AIAgent)
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    
    with patch("app.workers.main_worker.AsyncSessionLocal", return_value=MagicMock(__aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock())):
        await process_message(payload, mock_agent)
        
    assert "Ticket not found in database" in caplog.text

@pytest.mark.asyncio
async def test_process_message_ai_failure(caplog):
    ticket_id = str(uuid.uuid4())
    payload = {"ticket_id": ticket_id, "subject": "Test"}
    
    mock_agent = MagicMock(spec=AIAgent)
    mock_agent.process_ticket.side_effect = Exception("AI Timeout")
    
    mock_ticket = MagicMock()
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_ticket
    mock_session.execute.return_value = mock_result
    
    with patch("app.workers.main_worker.AsyncSessionLocal", return_value=MagicMock(__aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock())):
        await process_message(payload, mock_agent)
        
    assert "AI Agent processing failed" in caplog.text
    # Status should NOT be updated
    assert mock_ticket.status != "AI_PROCESSED"
