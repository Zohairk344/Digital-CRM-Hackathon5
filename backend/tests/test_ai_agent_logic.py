import pytest
from app.ai.agent import SupportTicket, TicketAnalysis, SentimentLabelEnum, CategoryEnum

def test_pydantic_validation():
    """Verify that the TicketAnalysis model validates fields correctly."""
    analysis = TicketAnalysis(
        category=CategoryEnum.TECHNICAL,
        sentiment_label=SentimentLabelEnum.POSITIVE,
        sentiment_score=0.9,
        is_escalated=False,
        suggested_response="Test response"
    )
    assert analysis.category == "Technical"
    assert analysis.sentiment_score == 0.9

def test_constitution_escalation_sentiment():
    """Verify that sentiment < 0.3 forces is_escalated to True."""
    # Case 1: sentiment < 0.3, is_escalated initially False
    analysis = TicketAnalysis(
        category=CategoryEnum.TECHNICAL,
        sentiment_label=SentimentLabelEnum.NEGATIVE,
        sentiment_score=0.2,
        is_escalated=False,
        suggested_response="Frustrated customer"
    )
    assert analysis.is_escalated is True, "Should be escalated due to sentiment score < 0.3"

    # Case 2: sentiment >= 0.3, is_escalated False
    analysis = TicketAnalysis(
        category=CategoryEnum.GENERAL,
        sentiment_label=SentimentLabelEnum.NEUTRAL,
        sentiment_score=0.5,
        is_escalated=False,
        suggested_response="Neutral customer"
    )
    assert analysis.is_escalated is False

def test_enum_strictness():
    """Verify that invalid enums raise validation errors."""
    with pytest.raises(ValueError):
        TicketAnalysis(
            category="InvalidCategory",
            sentiment_label=SentimentLabelEnum.POSITIVE,
            sentiment_score=0.8,
            is_escalated=False,
            suggested_response="..."
        )

if __name__ == "__main__":
    # Simple manual run
    print("Running manual logic tests...")
    test_pydantic_validation()
    test_constitution_escalation_sentiment()
    print("✅ Logic tests passed!")
