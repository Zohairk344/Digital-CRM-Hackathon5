# Data Model: Web Support Form Channel

## Entities

### Customer (Existing)
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed)
- `phone`: String (Optional, Unique, Indexed)
- `name`: String (Stored in metadata or added if schema allows - *Note: Existing model doesn't have 'name' field, will store in metadata or assume user wants it in metadata*)
- `is_active`: Boolean (Default: True)

### Ticket (Existing)
- `id`: UUID (Primary Key)
- `customer_id`: UUID (Foreign Key to Customer)
- `status`: String (Default: 'open')
- `priority`: String (low, medium, high, urgent)
- `channel_origin`: String ('web')
- `metadata_json`: JSONB (Stores category and tags)

### Message (Existing)
- `id`: UUID (Primary Key)
- `ticket_id`: UUID (Foreign Key to Ticket)
- `sender_type`: String ('customer')
- `channel`: String ('web')
- `content`: Text
- `sentiment_score`: Float
- `metadata_json`: JSONB

### OutboxEvent (Existing)
- `id`: UUID (Primary Key)
- `event_type`: String ('ticket.created')
- `payload`: JSONB (Contains ticket details)
- `status`: String (pending, processed, failed)

## Relationships
- One **Customer** has many **Tickets**.
- One **Ticket** has many **Messages**.
- One **Ticket** results in one **OutboxEvent** (on creation).

## Validation Rules
- **Email**: Must be valid format.
- **Message**: Cannot be empty.
- **Category/Priority**: Must be from predefined set.
