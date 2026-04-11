# Research: CRM Database Foundations

## Key Decisions

### 1. ORM: SQLAlchemy 2.0 (Async)
- **Decision**: Use SQLAlchemy 2.0 with `asyncio` and `asyncpg`.
- **Rationale**: Best-in-class performance for async Python. Native support for Pydantic v2 via `TypeAdapter` if needed.
- **Alternatives**: Tortoise ORM (simpler but less powerful/standard), SQLModel (Great for simpler models, but SQLAlchemy offers more granular control over complex relationships).

### 2. Identifier Strategy: UUIDs
- **Decision**: Use `UUID` (v4) for all primary keys.
- **Rationale**: Prevents ID enumeration attacks, allows for client-side generation, and simplifies distributed ID management.
- **Alternatives**: Sequential Integers (less secure, prone to enumeration), ULIDs (lexicographically sortable but less standard in Postgres).

### 3. Vector Search: pgvector (1536-dim)
- **Decision**: Implement `pgvector` with 1536 dimensions for `KnowledgeArticle.embedding`.
- **Rationale**: Matches standard OpenAI `text-embedding-3-small` dimensions. Allows storing and searching embeddings within the same relational DB, reducing architectural complexity.
- **Alternatives**: Pinecone/Milvus (External vector DBs - overkill for this MVP stage).

### 4. Timestamp Strategy: Global UTC
- **Decision**: Store all datetime fields as UTC and ensure app-level conversion to UTC before persistence.
- **Rationale**: Eliminates timezone bugs and simplifies cross-region reporting.

### 5. Extensibility: JSONB Metadata
- **Decision**: Add `metadata` (JSONB) to `Ticket` and `Message` entities.
- **Rationale**: Allows storing channel-specific data (e.g., WhatsApp message IDs, Gmail thread IDs, or custom agent tags) without modifying the schema for every new integration.

### 6. Data Deletion: Soft Deletion
- **Decision**: Implement soft deletion using `is_active` (Boolean) and `deleted_at` (DateTime) columns for `Customer`, `Ticket`, and `Message`.
- **Rationale**: Prevents accidental data loss while still allowing records to be effectively "removed" from the active interface.

### 7. Performance: Composite Indexing
- **Decision**: Define composite indexes for `Message(ticket_id, created_at DESC)` and `Ticket(customer_id, created_at DESC)`.
- **Rationale**: Ensures the database layer is "performance-ready" for its core access patterns (customer lookup and chronological message retrieval) from day one.

## Best Practices

### Dependency Management (uv)
- Use `uv add fastapi sqlalchemy asyncpg pydantic-settings pgvector pytest pytest-asyncio`
- Maintain `uv.lock` for deterministic builds.

### Database Connection (SQLAlchemy Async)
- Use `create_async_engine` with `pool_pre_ping=True` for reliability.
- Configure `async_sessionmaker` for transaction management.

### Entity Uniqueness (Customer)
- Implement `CheckConstraint` at the DB level to enforce `email IS NOT NULL OR phone IS NOT NULL`.
- Apply `UniqueConstraint` on both email and phone fields.
