import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import get_db
from unittest.mock import AsyncMock, MagicMock
import uuid

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    # session.begin should return an async context manager
    cm = AsyncMock()
    cm.__aenter__ = AsyncMock(return_value=cm)
    cm.__aexit__ = AsyncMock(return_value=None)
    
    # Use MagicMock for begin so it's not a coroutine
    session.begin = MagicMock(return_value=cm)
    return session

@pytest.fixture
def override_get_db(mock_db_session):
    async def _get_db():
        yield mock_db_session
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.pop(get_db, None)

@pytest.mark.asyncio
async def test_submit_web_form_success(mock_db_session, override_get_db, mocker):
    """
    Test successful submission of the web support form with mocks.
    Verifies US1, US2 (status codes), and US3 (basic creation logic).
    """
    # Mock CRUD functions
    mocker.patch("app.db.crud.get_customer_by_email", return_value=AsyncMock(id=uuid.uuid4()))
    mocker.patch("app.db.crud.create_ticket", return_value=AsyncMock(id=uuid.uuid4(), priority="medium", metadata_json={}))
    mocker.patch("app.db.crud.create_message", return_value=AsyncMock())
    mocker.patch("app.db.crud.create_outbox_event", return_value=AsyncMock())
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "category": "Bug Report",
            "priority": "medium",
            "message": "I found a bug in the dashboard."
        }
        response = await ac.post("/api/v1/webhooks/web-form", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "ticket_id" in data
        
        # Verify transaction was used
        mock_db_session.begin.assert_called_once()

@pytest.mark.asyncio
async def test_submit_web_form_pricing_escalation(mock_db_session, override_get_db, mocker):
    """
    Test that messages with pricing keywords are escalated (FR-C1).
    """
    mocker.patch("app.db.crud.get_customer_by_email", return_value=AsyncMock(id=uuid.uuid4()))
    mock_create_ticket = mocker.patch("app.db.crud.create_ticket", return_value=AsyncMock(id=uuid.uuid4()))
    mocker.patch("app.db.crud.create_message", return_value=AsyncMock())
    mocker.patch("app.db.crud.create_outbox_event", return_value=AsyncMock())
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "category": "General",
            "priority": "low",
            "message": "Can you give me a discount or a quote?"
        }
        response = await ac.post("/api/v1/webhooks/web-form", json=payload)
        
        assert response.status_code == 201
        # Verify ticket was created with urgent priority
        mock_create_ticket.assert_called_once()
        args, kwargs = mock_create_ticket.call_args
        assert kwargs["priority"] == "urgent"
        assert "pricing_escalation" in kwargs["metadata_json"]["tags"]

@pytest.mark.asyncio
async def test_submit_web_form_negative_sentiment_escalation(mock_db_session, override_get_db, mocker):
    """
    Test that messages with negative sentiment are escalated (FR-C2).
    """
    mocker.patch("app.db.crud.get_customer_by_email", return_value=AsyncMock(id=uuid.uuid4()))
    mock_create_ticket = mocker.patch("app.db.crud.create_ticket", return_value=AsyncMock(id=uuid.uuid4()))
    mocker.patch("app.db.crud.create_message", return_value=AsyncMock())
    mocker.patch("app.db.crud.create_outbox_event", return_value=AsyncMock())
    
    # Mock get_sentiment_score to return low score
    mocker.patch("app.api.v1.webhooks.web_form.get_sentiment_score", return_value=0.1)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "category": "General",
            "priority": "low",
            "message": "This is terrible!"
        }
        response = await ac.post("/api/v1/webhooks/web-form", json=payload)
        
        assert response.status_code == 201
        # Verify ticket was created with urgent priority
        args, kwargs = mock_create_ticket.call_args
        assert kwargs["priority"] == "urgent"
        assert "negative_sentiment" in kwargs["metadata_json"]["tags"]

@pytest.mark.asyncio
async def test_submit_web_form_failure_rollback(mock_db_session, override_get_db, mocker):
    """
    Test that an exception triggers a 500 response.
    """
    # Simulate an error during ticket creation
    mocker.patch("app.db.crud.get_customer_by_email", return_value=AsyncMock(id=uuid.uuid4()))
    mocker.patch("app.db.crud.create_ticket", side_effect=Exception("DB Error"))
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "category": "General",
            "priority": "low",
            "message": "Help me"
        }
        response = await ac.post("/api/v1/webhooks/web-form", json=payload)
        
        assert response.status_code == 500
        data = response.json()
        assert "error" in data["detail"].lower()
