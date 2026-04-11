# Feature Specification: Web Support Form Channel

**Feature Branch**: `052-web-support-form`  
**Created**: 2026-03-28  
**Status**: Draft  
**Input**: User description: "Build \"Feature 2: Web Support Form Channel\". This feature includes a standalone Next.js frontend component where customers can submit support requests, and a FastAPI backend endpoint to process these submissions. The backend must use the previously built CRUD operations to safely store the incoming request in the PostgreSQL database. [TECH STACK] - Frontend: Next.js 14+ (App Router), TypeScript, Tailwind CSS. - Backend: FastAPI (Python 3.12+), SQLAlchemy (Async), Pydantic v2. - Package Managers: npm (Frontend), uv (Backend). [FRONTEND REQUIREMENTS (Next.js)] 1. **SupportForm Component:** Create a modern, responsive React client component (SupportForm.tsx). 2. **Form Fields:** - Name (Text, required) - Email (Email, required) - Crucial for cross-channel identification - Phone (Tel, optional) - Category (Select/Dropdown: 'General', 'Bug Report', 'Feature Request', 'Billing') - Priority (Select/Dropdown: 'low', 'medium', 'high') - Message (Textarea, required) 3. **UX/UI State:** - Handle loading states (disable submit button, show spinner). - Display success message containing the newly created Ticket ID upon successful submission. - Display clear error messages if the submission fails. [BACKEND REQUIREMENTS (FastAPI)] 1. **API Endpoint:** Create a POST /api/v1/webhooks/web-form endpoint in FastAPI. 2. **Data Validation:** Create a Pydantic schema (WebFormSubmission) to validate the incoming JSON payload from the frontend. 3. **Database Operations (using existing crud.py):** - Customer: Look up the customer by email. If they don't exist, create a new Customer record. - Ticket: Create a new Ticket linked to the customer. Set channel_origin to 'web' and status to 'open'. - Message: Create a new Message linked to the ticket containing the user's text. Set sender_type to 'customer' and channel to 'web'. - Outbox/Kafka Prep: If an OutboxEvent model exists from Feature 1, log this new ticket creation as an event so the Kafka producer can pick it up later. 4. **Response:** Return the created ticket_id and a success status to the frontend. [EDGE CASES & CORS] - CORS: Ensure the FastAPI app has CORSMiddleware configured to accept requests from the Next.js local development server (typically http://localhost:3000). - Database Rollbacks: The endpoint must execute the Customer, Ticket, and Message creation within a single asynchronous database transaction. If any step fails, the entire transaction must roll back to prevent orphaned records."

## Clarifications

### Session 2026-03-28

- Q: How should the system "escalate" messages with sentiment score < 0.3? → A: Set ticket priority to 'urgent' and tag as 'negative-sentiment'
- Q: How should the system "escalate to human" for pricing/competitor queries? → A: Set ticket priority to 'high' and add 'pricing-competitor' tag
- Q: If a new Customer record is created, should the Phone number (if provided) be stored on the Customer entity? → A: Yes, store phone on Customer record

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Customer Submits a Web Support Request (Priority: P1)

A website visitor needs assistance and uses the web support form to submit their request. They want immediate confirmation that their request was received.

**Why this priority**: This is the core functionality of the web support channel, enabling customers to initiate contact and receive a ticket ID for tracking.

**Independent Test**: A user navigates to the support form, fills in all required fields, and clicks submit. The system displays a success message with a Ticket ID. In the database, a new Ticket, Customer (if new), and Message are created and linked correctly.

**Acceptance Scenarios**:

1. **Given** a customer is on the support form page, **When** they fill in all required fields (Name, Email, Category, Priority, Message) and click "Submit", **Then** they see a success message with a unique Ticket ID.
2. **Given** a new customer (email not in system), **When** they submit the form, **Then** a new Customer record is created along with the Ticket and Message.
3. **Given** an existing customer (email already in system), **When** they submit the form, **Then** the new Ticket and Message are linked to their existing record.

---

### User Story 2 - Form Validation and User Feedback (Priority: P2)

A customer makes a mistake while filling out the form. They need clear guidance on what is missing or incorrect to successfully submit their request.

**Why this priority**: Prevents invalid data from reaching the backend and improves user experience by providing immediate feedback.

**Independent Test**: A user attempts to submit the form with empty required fields or an invalid email format. The system prevents submission and highlights the errors.

**Acceptance Scenarios**:

1. **Given** the support form, **When** a user clicks "Submit" with empty required fields, **Then** the system prevents submission and displays validation errors for each missing field.
2. **Given** the support form, **When** a user enters an invalid email format, **Then** the system displays an "Invalid email" error and prevents submission.
3. **Given** a submission is in progress, **When** the user clicks "Submit", **Then** the submit button is disabled and a loading spinner is shown until the response is received.

---

### User Story 3 - System Resilience and Data Integrity (Priority: P3)

The system encounters a temporary failure during processing. The customer's request should not be partially saved, and they should be informed of the failure.

**Why this priority**: Ensures database consistency and informs the user when they need to try again or contact support via another channel.

**Independent Test**: Simulate a database failure during the ticket creation step. Verify that no Customer or Message records are left orphaned in the database and the user sees a clear error message.

**Acceptance Scenarios**:

1. **Given** a backend error occurs during submission, **When** the user clicks "Submit", **Then** the system displays a clear error message and no partial data is committed to the database.

---

### Edge Cases

- **Duplicate Submissions**: If a user double-clicks the submit button, only one ticket should be created.
- **Large Message Content**: How does the system handle extremely long messages? (Assumption: Standard textarea limits apply, but system should handle reasonable lengths).
- **Concurrent Submissions with same email**: Two users (or one user in two tabs) submitting with the same new email simultaneously.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a responsive React client component (`SupportForm.tsx`) using Next.js 14+ App Router.
- **FR-002**: The form MUST capture: Name (required), Email (required), Phone (optional), Category (dropdown: 'General', 'Bug Report', 'Feature Request', 'Billing'), Priority (dropdown: 'low', 'medium', 'high'), and Message (required).
- **FR-003**: The system MUST validate the Email format on both frontend and backend.
- **FR-004**: The system MUST handle loading states by disabling the submit button and showing a spinner during processing.
- **FR-005**: The system MUST provide a FastAPI endpoint `POST /api/v1/webhooks/web-form` to process submissions.
- **FR-006**: The backend MUST look up the Customer by email; if not found, it MUST create a new Customer record including the Name and Phone (if provided).
- **FR-007**: The backend MUST create a new Ticket linked to the Customer with `channel_origin='web'` and `status='open'`.
- **FR-008**: The backend MUST create a new Message linked to the Ticket with `sender_type='customer'`, `channel='web'`, and the user's message text.
- **FR-009**: The backend MUST execute all database operations (Customer, Ticket, Message) within a single asynchronous transaction with rollback support.
- **FR-010**: The backend MUST log an `OutboxEvent` for the new ticket if the model exists.
- **FR-011**: The system MUST configure CORS to allow requests from `http://localhost:3000`.

**Constitution Mandatory Requirements:**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries by setting ticket priority to 'high' and adding a 'pricing-competitor' tag.
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3 by setting ticket priority to 'urgent' and adding a 'negative-sentiment' tag.
- **FR-C4**: All state MUST be persisted in PostgreSQL.
- **FR-C5**: All events MUST be processed through Kafka/Redpanda.

### Key Entities *(include if feature involves data)*

- **Customer**: Represents the person submitting the form. Linked by email.
- **Ticket**: The support request container. Linked to a Customer.
- **Message**: The actual text submitted by the customer. Linked to a Ticket.
- **OutboxEvent**: Record of the ticket creation for asynchronous processing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete and submit the support form in under 60 seconds on average.
- **SC-002**: 100% of successful submissions return a valid Ticket ID to the frontend within 2 seconds.
- **SC-003**: 100% of submissions from new emails result in exactly one new Customer record.
- **SC-004**: System successfully rolls back 100% of partial changes if any step in the creation transaction fails.
ck 100% of partial changes if any step in the creation transaction fails.
tep in the creation transaction fails.
ck 100% of partial changes if any step in the creation transaction fails.
