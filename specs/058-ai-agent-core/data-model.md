# Data Model: AI Agent Core (Feature 4.1)

## Entities

### `SupportTicket` (Input)
Represents the incoming ticket to be analyzed.
- `ticket_id`: (string) Unique ID of the ticket.
- `subject`: (string) The ticket subject line.
- `description`: (string) The full ticket body.

### `TicketAnalysis` (Output)
Represents the structured analysis of the ticket by the AI.
- `category`: (enum: Billing, Technical, Product, Feature Request, General)
- `sentiment_label`: (enum: Positive, Neutral, Negative)
- `sentiment_score`: (float: 0.0 to 1.0)
- `is_escalated`: (boolean: True if pricing/competitor query OR sentiment < 0.3)
- `suggested_response`: (string: The drafted response for the user)

## Validation Rules
- `sentiment_score` must be between 0.0 and 1.0.
- `is_escalated` must be `True` if `sentiment_score` < 0.3.
- `category` must be one of the specified enum values.
- `suggested_response` must be non-empty and formatted with bullet points for actions.
