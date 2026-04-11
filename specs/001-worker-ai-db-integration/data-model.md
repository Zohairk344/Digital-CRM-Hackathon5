# Data Model: Worker & DB Integration

## Entity: Ticket (Updated)

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| customer_id | UUID | Foreign Key to Customer |
| status | String | Current status (e.g., `open`, `AI_PROCESSED`) |
| priority | String | Priority (e.g., `low`, `medium`, `high`) |
| channel_origin | String | Origin (e.g., `web`, `gmail`, `whatsapp`) |
| category | String (New) | AI-determined category |
| suggested_response | Text (New) | AI-drafted response in bullet points |
| is_escalated | Boolean (New) | Flag for human intervention |
| metadata_json | JSONB | Additional unstructured data |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## State Transitions
- `PENDING` -> `AI_PROCESSED` (Success)
- `PENDING` -> `PENDING` (Failure, remains for retry)
