# Research: AI Agent Core (Feature 4.1)

## Decision 1: Structured Output Implementation
- **Decision**: Use `langchain_google_genai.ChatGoogleGenerativeAI` with `.with_structured_output(TicketAnalysis)`.
- **Rationale**: This ensures the LLM returns a validated Pydantic object. It leverages Gemini's native structured output capabilities to guarantee schema compliance.
- **Alternatives considered**: 
    - `langchain_openai`: Originally planned, but swapped to Gemini as per updated user requirements.

## Decision 2: Escalation Logic (is_escalated)
- **Decision**: Perform a two-tiered escalation check. The LLM will be instructed in the system prompt to identify pricing/competitor queries and highly negative sentiment, but the Python class will also have a secondary validation method to ensure constitutional thresholds (Sentiment < 0.3) are strictly enforced even if the LLM wavers.
- **Rationale**: Ensures compliance with the Hackathon 5 Constitution (FTE Handbook).

## Decision 3: Model Choice
- **Decision**: Use `gemini-1.5-flash`.
- **Rationale**: It provides high performance and low latency for classification tasks, making it ideal for a high-volume support ticket environment.
- **Alternatives considered**: `gemini-1.5-pro` (more powerful but potentially slower for this specific use case).

## Decision 4: Prompt Strategy
- **Decision**: Use a `ChatPromptTemplate` with a `SystemMessage` defining the "Expert Customer Support Agent" persona.
- **Rationale**: Standard LangChain pattern.
