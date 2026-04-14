# Omnichannel Webhooks Expansion - Plan

## Objective
Expand the Digital FTE backend to support Gmail and WhatsApp webhook endpoints for receiving customer inquiries, enabling cross-channel customer identification through an omnichannel architecture.

---

## Technical Steps

### 1. Create Gmail Webhook Router
- **File:** `backend/app/api/v1/webhooks/gmail.py`
- **Request Model:** `GmailPayload` with `sender_email` (EmailStr), `subject` (str), `body` (str)
- **Endpoint:** `POST /api/v1/webhooks/gmail`
- **Logic:**
  1. Normalize email (lowercase)
  2. Run sentiment analysis on `body`
  3. Customer lookup: Try `crud.get_customer_by_email()`, create if not exists
  4. Create Ticket: `channel_origin="GMAIL"`, priority based on sentiment/escalation logic
  5. Create Message: `channel="gmail"`, content=`body`
  6. Create OutboxEvent: Schema matching web_form with `channel="gmail"`

### 2. Create WhatsApp Webhook Router
- **File:** `backend/app/api/v1/webhooks/whatsapp.py`
- **Request Model:** `WhatsAppPayload` with `phone_number` (str), `message` (str), `name` (str)
- **Endpoint:** `POST /api/v1/webhooks/whatsapp`
- **Logic:**
  1. Sanitize phone: Strip `+`, spaces, dashes → digits-only (e.g., `+1-234-567-8900` → `1234567890`)
  2. Run sentiment analysis on `message`
  3. Customer lookup: Try `crud.get_customer_by_phone()`, create if not exists
  4. Create Ticket: `channel_origin="WHATSAPP"`, subject=`"WhatsApp Message from {name}"`
  5. Create Message: `channel="whatsapp"`, content=`message`
  6. Create OutboxEvent: Schema matching web_form with `channel="whatsapp"`

### 3. Integrate into Main App
- **File:** `backend/app/main.py`
- **Changes:**
  1. Import new routers: `from app.api.v1.webhooks import gmail, whatsapp`
  2. Add routers: `app.include_router(gmail.router, prefix="/api/v1")`
  3. Add routers: `app.include_router(whatsapp.router, prefix="/api/v1")`

---

## Data Mapping

| Field | Gmail Source | WhatsApp Source |
|-------|-------------|-----------------|
| customer_id | `sender_email` (lowercased) | `phone_number` (sanitized to digits) |
| subject | `subject` | "WhatsApp Message from {name}" |
| description | `body` | `message` |
| channel_origin (DB) | "GMAIL" | "WHATSAPP" |
| channel (Kafka) | "gmail" | "whatsapp" |

---

## Kafka Payload Schema
Shared across all channels (Web Form, Gmail, WhatsApp):
```json
{
  "ticket_id": "uuid-string",
  "customer_id": "uuid-string",
  "channel": "web" | "gmail" | "whatsapp",
  "priority": "low|medium|high|urgent",
  "sentiment_score": 0.0-1.0
}
```

---

## Dependencies to Reuse
- `app.core.sentiment.get_sentiment_score`
- `app.db.crud` (create_customer, get_customer_by_email, get_customer_by_phone, create_ticket, create_message, create_outbox_event)
- `app.db.database.get_db`
- Pydantic models from existing `web_form.py`

---

## Validation Criteria

### 1. Unit Tests
- Test `GmailPayload` validation (valid/invalid emails)
- Test `WhatsAppPayload` validation
- Test phone sanitization logic

### 2. Integration Tests (API)
- `POST /api/v1/webhooks/gmail` returns 201, creates ticket in DB
- `POST /api/v1/webhooks/whatsapp` returns 201, creates ticket in DB

### 3. End-to-End Tests
- Submit Gmail webhook → Kafka message published → Worker processes → Ticket updated
- Submit WhatsApp webhook → Kafka message published → Worker processes → Ticket updated

### 4. Cross-Channel Identification Test
- Create customer via Gmail (email)
- Submit WhatsApp with same sanitized phone number
- Verify same customer record or linked record exists

---

## Constraints
- Do NOT modify existing worker logic (`app/workers/main_worker.py`)
- Do NOT modify database models
- Follow existing coding style and import patterns from `web_form.py`
- Use Pydantic for all request validation