# Feature Specification: CRM Database Foundations

**Feature Branch**: `050-crm-db-foundations`  
**Created**: 2026-03-24  
**Status**: Draft  
**Input**: Build the foundational Database configuration and SQLAlchemy ORM models for the CRM Digital FTE Factory.

## Clarifications

### Session 2026-03-24
- Q: Should we explicitly store the name of the embedding model used for knowledge articles? → A: Yes, add `embedding_model` string column (e.g., 'text-embedding-3-small').
- Q: Should the Ticket and Message entities include a JSONB metadata field for extensibility? → A: Yes, add `metadata` (JSONB) to `Ticket` and `Message`.
- Q: Should we implement soft deletion for core entities? → A: Yes, implement Soft Deletion via `is_active` (Boolean) and `deleted_at` (DateTime) columns for Customer, Ticket, and Message.
- Q: Should we explicitly define requirements for specific performance-critical indexes? → A: Yes, define composite indexes for `Message(ticket_id, created_at)` and `Ticket(customer_id, created_at)` to support rapid retrieval of history.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Channel Customer Identification (Priority: P1)

As a system, I need to uniquely identify customers contacting us through different channels (WhatsApp, Gmail, Web) so that we can maintain a consistent history of their interactions regardless of how they reach out.

**Why this priority**: This is the foundation of the CRM. Without consistent customer identification, cross-channel support is impossible.

**Independent Test**: Create a customer with only an email, then attempt to create one with only a phone number, and finally attempt to create one with neither (which should fail).

**Acceptance Scenarios**:

1. **Given** a new contact from Gmail, **When** the system attempts to create a customer record with an email, **Then** a unique customer ID is generated.
2. **Given** a new contact from WhatsApp, **When** the system attempts to create a customer record with a phone number, **Then** a unique customer ID is generated.
3. **Given** a request to create a customer, **When** both email and phone are missing, **Then** the system rejects the creation with a validation error.

---

### User Story 2 - Ticket Lifecycle Management (Priority: P1)

As a support agent, I want to track the lifecycle of a customer issue through tickets with defined statuses and priorities so that no customer request is lost or ignored.

**Why this priority**: Essential for managing work and ensuring that all customer requests are addressed systematically.

**Independent Test**: Create a ticket for an existing customer and verify it can be updated through all status and priority levels.

**Acceptance Scenarios**:

1. **Given** an identified customer, **When** a new ticket is opened, **Then** it is saved with a status, priority, and channel origin.
2. **Given** an existing ticket, **When** its status or priority is updated, **Then** the changes are persisted and the 'updated_at' timestamp is refreshed.

---

### User Story 3 - Unified Message History (Priority: P2)

As a support agent, I want to see all messages for a specific ticket in a single chronological view, including the sentiment of the customer's messages.

**Why this priority**: Provides the necessary context for agents to resolve tickets effectively.

**Independent Test**: Log multiple messages to a single ticket and retrieve them to verify chronological ordering and metadata accuracy.

**Acceptance Scenarios**:

1. **Given** an active ticket, **When** a message is received or sent, **Then** it is stored with sender type, channel, content, and sentiment score.
2. **Given** a ticket history, **When** retrieved, **Then** all messages are returned in chronological order.

---

### User Story 4 - Knowledge Base for AI Agents (Priority: P2)

As an AI Digital FTE, I need to access a knowledge base of articles with semantic search capabilities so that I can provide accurate answers based on existing documentation.

**Why this priority**: Critical for enabling automated, AI-driven support that leverages a shared knowledge base.

**Independent Test**: Store a knowledge article with its vector embedding and perform a semantic search to retrieve it.

**Acceptance Scenarios**:

1. **Given** a knowledge article, **When** it is saved, **Then** it includes a vector embedding for semantic search.
2. **Given** a search query, **When** processed semantically, **Then** relevant articles are returned based on embedding similarity.

### Edge Cases

- **Identifier Conflict**: A customer with email 'A' later contacts via phone 'B'. These are treated as separate customers unless linked.
- **Connection Drops**: Temporary database unavailability during an operation must be handled gracefully.
- **Nullability**: Preventing the creation of a customer record if both email and phone are null.
- **Deletion Restriction**: Preventing deletion of a Customer if they have existing Tickets or Messages.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST uniquely identify customers using a UUID as the primary key.
- **FR-002**: System MUST allow customer identification via either a unique email or a unique phone number.
- **FR-003**: System MUST enforce that at least one identifier (email or phone) is present for every customer record.
- **FR-004**: System MUST track tickets with a status enum: 'open', 'in_progress', 'resolved', 'escalated'.
- **FR-005**: System MUST track tickets with a priority enum: 'low', 'medium', 'high'.
- **FR-006**: System MUST record the origin channel of every ticket: 'web', 'gmail', 'whatsapp'.
- **FR-007**: System MUST log messages with sender type (customer/agent), channel, content, and sentiment score (0.0 to 1.0).
- **FR-008**: System MUST store knowledge articles with titles, text content, vector embeddings (size 1536), and the associated `embedding_model` name.
- **FR-009**: System MUST handle database connection drops gracefully using connection pooling and health checks (pre-ping).
- **FR-010**: System MUST store all database datetime fields in UTC format.
- **FR-011**: System MUST enforce referential integrity (RESTRICT on delete) for Customer -> Ticket relationship.
- **FR-012**: System MUST include a `metadata` JSONB field in `Ticket` and `Message` entities for integration-specific data storage.
- **FR-013**: System MUST support soft deletion for Customer, Ticket, and Message entities using `is_active` (boolean) and `deleted_at` (UTC timestamp) fields.
- **FR-014**: System MUST implement database indexes for `Message(ticket_id, created_at DESC)` and `Ticket(customer_id, created_at DESC)` to optimize history retrieval.
- **FR-015**: System MUST include an `OutboxEvent` table to store state changes intended for Kafka, ensuring atomicity (Constitution FR-C5).

**Constitution Mandatory Requirements:**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries (Handled at application layer, but supported by schema).
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3 (Handled at application layer, but sentiment score stored in schema).
- **FR-C3**: WhatsApp responses MUST be < 300 characters (Handled at application layer, but channel logged in schema).
- **FR-C4**: All state MUST be persisted in PostgreSQL.
- **FR-C5**: All events MUST be processed through Kafka/Redpanda (Database stores the resulting state).

### Key Entities *(include if feature involves data)*

- **Customer**: Represents an individual user. Attributes: id (UUID), email (nullable, unique), phone (nullable, unique), created_at, is_active (Boolean), deleted_at (Nullable DateTime).
- **Ticket**: Represents a support request. Attributes: id (UUID), customer_id, status, priority, channel_origin, created_at, updated_at, metadata (JSONB), is_active (Boolean), deleted_at (Nullable DateTime).
- **Message**: An individual interaction. Attributes: id (UUID), ticket_id, sender_type, channel, content, sentiment_score, created_at, metadata (JSONB), is_active (Boolean), deleted_at (Nullable DateTime).
- **KnowledgeArticle**: Reference documentation. Attributes: id (UUID), title, content, embedding (Vector 1536), embedding_model (String).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of customer records satisfy the "email OR phone" constraint.
- **SC-002**: Database schema supports 1536-dimensional vector embeddings for knowledge articles.
- **SC-003**: System recovers from transient database connection failures (defined as <5s disconnects) without data loss via connection pooling and pre-ping health checks.
- **SC-004**: Querying a ticket returns a complete, chronological history of messages across all integrated channels.
- **SC-005**: Referential integrity ensures Customers cannot be deleted while they have active Tickets.
