# Quickstart: AI Agent Core (Feature 4.1)

## Environment Setup
1.  Navigate to the `/backend` directory:
    ```bash
    cd backend
    ```
2.  Install the required dependencies using `uv`:
    ```bash
    uv add langchain langchain-openai openai pydantic
    ```
3.  Ensure your `.env` file contains a valid `OPENAI_API_KEY`:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

## Execution
Run the isolated AI agent script to test the analysis logic:
```bash
uv run python -m app.ai.agent
```

## Expected Output
A successful run will print a structured `TicketAnalysis` object:
```python
{
  "category": "Technical",
  "sentiment_label": "Negative",
  "sentiment_score": 0.2,
  "is_escalated": True,
  "suggested_response": "..."
}
```
