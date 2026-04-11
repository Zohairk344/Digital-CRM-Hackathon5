# Data Model: Support Form

## Entities

### SupportTicketRequest
Represented by the form input fields and validated by Zod schema.

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| name | string | min(2) | User's full name |
| email | string | email() | User's contact email |
| phone | string (optional) | - | User's phone number |
| category | enum | ['General', 'Bug Report', 'Feature Request', 'Billing'] | Category of the request |
| priority | enum | ['low', 'medium', 'high', 'urgent'] | Urgency level |
| message | string | min(10) | Detailed support request |

### SupportTicketResponse
Data returned from the API upon successful submission.

| Field | Type | Description |
|-------|------|-------------|
| ticket_id | string | Unique identifier for the created ticket |
| status | string | Submission status (e.g., "success") |

## State Transitions

- **Idle**: Initial form state.
- **Loading**: Form is being submitted via fetch.
- **Success**: Submission complete; ticket_id received and displayed.
- **Error**: Submission failed; error message displayed to user.
