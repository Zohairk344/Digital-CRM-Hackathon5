# Data Model: CRM Foundations

## Entities

### 1. Customer
Represents an individual user across multiple channels.
- `id`: UUID (v4) - Primary Key
- `email`: String(255) - Unique, Nullable
- `phone`: String(20) - Unique, Nullable
- `created_at`: DateTime (UTC)
- `is_active`: Boolean - Default: True
- `deleted_at`: DateTime (UTC) - Nullable
- **Relationships**: One-to-Many with `Ticket`
- **Constraints**: `CHECK (email IS NOT NULL OR phone IS NOT NULL)`

### 2. Ticket
Represents a support request or conversation thread.
- `id`: UUID (v4) - Primary Key
- `customer_id`: UUID - Foreign Key (Customer.id)
- `status`: Enum ('open', 'in_progress', 'resolved', 'escalated')
- `priority`: Enum ('low', 'medium', 'high')
- `channel_origin`: Enum ('web', 'gmail', 'whatsapp')
- `created_at`: DateTime (UTC)
- `updated_at`: DateTime (UTC)
- `is_active`: Boolean - Default: True
- `deleted_at`: DateTime (UTC) - Nullable
- `metadata`: JSONB - Nullable
- **Relationships**: Many-to-One with `Customer`, One-to-Many with `Message`
- **Constraints**: `RESTRICT` on delete for `customer_id`
- **Indexes**: `Index('idx_ticket_customer_created', customer_id, created_at.desc())`

### 3. Message
A single interaction within a ticket.
- `id`: UUID (v4) - Primary Key
- `ticket_id`: UUID - Foreign Key (Ticket.id)
- `agent_id`: UUID - Nullable (Link to AI Worker or Human Agent)
- `sender_type`: Enum ('customer', 'agent')
- `channel`: Enum ('web', 'gmail', 'whatsapp')
- `content`: Text
- `sentiment_score`: Float (0.0 to 1.0)
- `created_at`: DateTime (UTC)
- `is_active`: Boolean - Default: True
- `deleted_at`: DateTime (UTC) - Nullable
- `metadata`: JSONB - Nullable
- **Relationships**: Many-to-One with `Ticket`
- **Constraints**: `CASCADE` on delete for `ticket_id`
- **Indexes**: `Index('idx_message_ticket_created', ticket_id, created_at.desc())`

### 4. KnowledgeArticle
Reference documentation with semantic search.
- `id`: UUID (v4) - Primary Key
- `title`: String(255)
- `content`: Text
- `embedding`: Vector(1536)
- `embedding_model`: String(100) - e.g., 'text-embedding-3-small'
- `created_at`: DateTime (UTC)
- `updated_at`: DateTime (UTC)

## State Transitions

### Ticket Status
- `open` -> `in_progress` (Assigned)
- `in_progress` -> `resolved` (Completed)
- `in_progress` -> `escalated` (Human intervention)
- `escalated` -> `in_progress` (Resolved/Handled)
- `resolved` -> `open` (Re-opened)
