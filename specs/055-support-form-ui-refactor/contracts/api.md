# API Contract: Support Form Submission

## POST /api/v1/webhooks/web-form

**Base URL**: `http://localhost:8000` (Assumed for local dev)

### Request Body (JSON)

```json
{
  "name": "string (min 2 characters)",
  "email": "string (valid email)",
  "phone": "string (optional)",
  "category": "General | Bug Report | Feature Request | Billing",
  "priority": "low | medium | high | urgent",
  "message": "string (min 10 characters)"
}
```

### Response Body (JSON - Success 200/201)

```json
{
  "ticket_id": "string",
  "status": "success",
  "message": "Request successfully received"
}
```

### Response Body (JSON - Error 4xx/5xx)

```json
{
  "detail": "string (error description)"
}
```

## Error Taxonomy

| Status Code | Description | User Message |
|-------------|-------------|--------------|
| 400 | Bad Request (Validation failure) | "Please check the form for errors." |
| 422 | Unprocessable Entity (Zod/Pydantic validation) | "Input data is invalid." |
| 500 | Internal Server Error | "An unexpected error occurred. Please try again later." |
