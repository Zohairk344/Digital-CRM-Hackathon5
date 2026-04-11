def get_sentiment_score(text: str) -> float:
    """
    A simple heuristic for sentiment analysis.
    Returns 0.1 if negative keywords are found, otherwise 1.0.
    """
    negative_keywords = ["angry", "broken", "terrible", "urgent"]
    text_lower = text.lower()
    
    for keyword in negative_keywords:
        if keyword in text_lower:
            return 0.1
            
    return 1.0
