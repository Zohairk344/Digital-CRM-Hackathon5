# Feature Specification: Web Support Form Channel

**Feature Branch**: `051-web-support-form`  
**Created**: 2026-03-24  
**Status**: Draft  
**Input**: User description: "Build ""Feature 2: Web Support Form Channel"". This feature includes a standalone Next.js frontend component where customers can submit support requests, and a FastAPI backend endpoint to process these submissions. The backend must use the previously built CRUD operations to safely store the incoming request in the PostgreSQL database. [TECH STACK] - Frontend: Next.js 14+ (App Router), TypeScript, Tailwind CSS. - Backend: FastAPI (Python 3.12+), SQLAlchemy (Async), Pydantic v2. - Package Managers: npm (Frontend), uv (Backend). [FRONTEND REQUIREMENTS (Next.js)] 1. **SupportForm Component:** Create a modern, responsive React client component (SupportForm.tsx). 2. **Form Fields:** - Name (Text, required) - Email (Email, required) - *Crucial for cross-channel identification* - Phone (Tel, optional) - Category (Select/Dropdown: 'General', 'Bug Report', 'Feature Request', 'Billing') - Priority (Select/Dropdown: 'low', 'medium', 'high') - Message (Textarea, required) 3. **UX/UI State:** - Handle loading states (disable submit button, show spinner). - Display success message containing the newly created Ticket ID upon successful submission. - Display clear error messages if the submission fails. [BACKEND REQUIREMENTS (FastAPI)] 1. **API Endpoint:** Create a POST /api/v1/webhooks/web-form endpoint in FastAPI. 2. **Data Validation:** Create a Pydantic schema (WebFormSubmission) to validate the incoming JSON payload from the frontend. 3. **Database Operations (using existing crud.py):** - **Customer:** Look up the customer by email. If they don't exist, create a new Customer record. - **Ticket:** Create a new Ticket linked to the customer. Set channel_origin to 'web' and status to 'open'. - **Message:** Create a new Message linked to the ticket containing the user's text. Set sender_type to 'customer' and channel to 'web'. - **Outbox/Kafka Prep:** If an OutboxEvent model exists from Feature 1, log this new ticket creation as an event so the Kafka producer can pick it up later. 4. **Response:** Return the created ticket_id and a success status to the frontend. [EDGE CASES & CORS] - **CORS:** Ensure the FastAPI app has CORSMiddleware configured to accept requests from the Next.js local development server (typically http://localhost:3000). - **Database Rollbacks:** The endpoint must execute the Customer, Ticket, and Message creation within a single asynchronous database transaction. If any step fails, the entire transaction must roll back to prevent orphaned records."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Customer Submits a Support Request (Priority: P1)

A customer visiting the website can fill out and submit a support form with their issue.

**Why this priority**: This is the core functionality of the feature, enabling the primary channel for web-based customer support.

**Independent Test**: A user can navigate to the support form, fill in the required fields, submit it, and receive a confirmation with a ticket ID. The submitted data should be correctly stored in the system and visible to support agents.

**Acceptance Scenarios**:

1. **Given** a customer is on the support page, **When** they fill in all required fields (Name, Email, Category, Priority, Message) and click "Submit", **Then** they see a success message with a unique Ticket ID, and a new ticket is created in the system.
2. **Given** a customer is on the support page, **When** they attempt to submit the form with a missing required field, **Then** they see an error message indicating which field is missing, and the form is not submitted.
3. **Given** a customer has submitted a support request, **When** an admin views the customer's record, **Then** a new ticket associated with that customer is visible with the status 'open' and channel 'web'.

---

### Edge Cases

- **Invalid Email**: What happens when the user submits the form with an invalid email format? The system should display an inline validation error and prevent submission.
- **System Failure**: What happens if the system is unable to connect to the database or another critical service when the form is submitted? The user should see a generic error message like "Something went wrong, please try again later."
- **Duplicate Submissions**: What happens if a user tries to submit the form multiple times in quick succession? The submit button should be disabled after the first click to prevent creating duplicate tickets.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a web form for customers to submit support requests.
- **FR-002**: The support form MUST capture the customer's Name, Email, Phone (optional), a support Category, a Priority level, and a Message.
- **FR-003**: The system MUST validate that Name, Email, Category, Priority, and Message are provided before accepting the submission.
- **FR-004**: The system MUST validate the format of the Email address.
- **FR-005**: Upon successful submission, the system MUST display a confirmation message to the user, including a unique Ticket ID.
- **FR-006**: The system MUST create a new customer record if the provided email does not already exist in the system.
- **FR-007**: The system MUST create a new support ticket linked to the customer, with a default status of 'open' and an origin channel of 'web'.
- **FR-008**: The system MUST store the user's message as part of the ticket, with the sender identified as 'customer'.
- **FR-009**: In case of a submission failure (e.g., server error), the system MUST display a clear error message to the user.
- **FR-010**: All data creation (Customer, Ticket, Message) for a single submission MUST be atomic. If one part fails, all changes must be rolled back to ensure data integrity.

### Key Entities *(include if feature involves data)*

- **Customer**: Represents an individual seeking support. Key attributes include Name, Email, and Phone.
- **Ticket**: Represents a single support request. Key attributes include a unique ID, the associated Customer, Status ('open', etc.), Priority ('low', 'medium', 'high'), Category ('General', etc.), and Origin Channel ('web').
- **Message**: Represents a communication within a ticket. Key attributes include the ticket it belongs to, the message content, the sender type ('customer' or 'agent'), and the channel ('web').

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid support form submissions are successfully stored in the system.
- **SC-002**: Users can complete and submit the support form in under 90 seconds on average.
- **SC-003**: The form submission success rate is greater than 99% for valid inputs.
- **SC-004**: Support agents can view and respond to tickets submitted through the web form within the support dashboard without needing to switch tools.
