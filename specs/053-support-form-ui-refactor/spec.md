# Feature Specification: Support Form UI/UX and Animations

**Feature Branch**: `053-support-form-ui-refactor`  
**Created**: 2026-03-31  
**Status**: Draft  
**Input**: User description: "[CONTEXT] Build \"Feature 2.1: Support Form UI/UX and Animations\". The functional logic for the Next.js Support Form (Feature 2.2) is already implemented and working perfectly using react-hook-form, zod, and native fetch. The objective of this feature is strictly to refactor the visual presentation to match a premium, modern SaaS application aesthetic. [TECH STACK] - Framework: Next.js 14+ (App Router) - Styling: Tailwind CSS v4 - Icons: lucide-react - Package Manager: npm (Frontend only) [UI/UX REQUIREMENTS] 1. Page Layout (app/support/page.tsx): - Create a professional, centered layout with a subtle background (e.g., a very light gray or a soft gradient). - Add a high-quality typographic header (e.g., \"Contact Customer Success\") and a brief, welcoming subtext. 2. Form Card (SupportForm.tsx): - Wrap the form in a clean white card container with soft shadows (shadow-xl), rounded corners (rounded-2xl), and spacious padding. 3. Input Fields and Typography: - Style all inputs, textareas, and select dropdowns with modern borders, rounded corners (rounded-lg), and clear, distinct focus states (e.g., a blue or indigo focus ring). - Use crisp, accessible typography for labels (small, medium-weight, dark gray). - Integrate lucide-react icons inside or adjacent to the input fields to provide visual cues (e.g., a User icon for Name, Mail icon for Email). 4. Interactive States and Animations (Tailwind Native): - Buttons: The submit button must have clear hover state transitions, active (click) states, and a disabled state that reduces opacity and shows a spinning loading icon when submitting. - Feedback: Success messages should appear as distinct, elegantly styled banners (e.g., soft green background with dark green text and a check icon). Error states on individual fields must be clearly highlighted in red with accompanying small red text. - Transitions: Use Tailwind transition-all duration-200 utilities to ensure all hover effects and focus rings animate smoothly rather than snapping instantly. [CONSTRAINTS AND SAFEGUARDS] - Zero Logic Changes: You MUST NOT alter the existing react-hook-form implementation, the zod schema, or the asynchronous fetch logic that communicates with the FastAPI backend. - Frontend Isolation: This feature is strictly confined to the /frontend directory. Do not propose any changes to the backend."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Premium Support Page Layout (Priority: P1)

As a customer seeking help, I want to land on a support page that looks professional and welcoming, so that I feel confident in the company's service quality.

**Why this priority**: The first impression of the support channel sets the tone for the customer's interaction with the company.

**Independent Test**: Can be tested by navigating to `/support` and verifying the centered layout, background styling, and header typography match the modern SaaS aesthetic.

**Acceptance Scenarios**:

1. **Given** a user navigates to `/support`, **When** the page loads, **Then** the layout is centered, the background is a subtle gray/gradient, and a clear typographic header "Contact Customer Success" is visible.
2. **Given** the support page is visible, **When** viewed on different screen sizes, **Then** the centered layout remains balanced and responsive.

---

### User Story 2 - Modernized Form Interaction (Priority: P2)

As a user filling out the support form, I want to see clear visual cues and smooth feedback when I interact with fields, so that the process feels intuitive and polished.

**Why this priority**: Enhances usability through functional icons and clear focus states, reducing cognitive load during form completion.

**Independent Test**: Can be tested by clicking into form fields and observing the focus rings, icons, and typographic styling of labels.

**Acceptance Scenarios**:

1. **Given** the support form, **When** a user clicks into an input field, **Then** a smooth blue or indigo focus ring appears via a 200ms transition.
2. **Given** the form fields, **When** viewed, **Then** each field has a corresponding icon (e.g., User for Name, Mail for Email) and labels use crisp, dark gray typography.

---

### User Story 3 - Interactive Feedback and States (Priority: P3)

As a user submitting my request, I want to see immediate and elegant feedback regarding the submission status, so that I know my request was received or if I need to correct errors.

**Why this priority**: Provides critical functional feedback through polished UI states, improving the overall user experience of the submission lifecycle.

**Independent Test**: Can be tested by submitting the form (valid and invalid cases) and observing the button animations, loading spinner, and success/error banners.

**Acceptance Scenarios**:

1. **Given** a valid form submission, **When** the submit button is clicked, **Then** it shows a spinning loading icon, becomes semi-opaque, and eventually displays a soft green success banner.
2. **Given** an invalid form field, **When** validation fails, **Then** the field is highlighted in red with small red error text appearing below it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present the support form within a white card container featuring `shadow-xl`, `rounded-2xl` corners, and spacious internal padding.
- **FR-002**: System MUST style all input fields, textareas, and select elements with modern borders, `rounded-lg` corners, and indigo/blue focus rings.
- **FR-003**: System MUST include `lucide-react` icons (e.g., User, Mail, MessageSquare) as visual cues for each primary input field.
- **FR-004**: System MUST implement a submit button with hover transitions, active click states, and a disabled loading state (reduced opacity + spinner).
- **FR-005**: System MUST display success feedback as a stylized banner with a green background, dark green text, and a check icon.
- **FR-006**: System MUST highlight field-level errors in red with accompanying descriptive text.
- **FR-007**: System MUST use Tailwind's `transition-all duration-200` utilities for all interactive element state changes (hover, focus, active).

**Constitution Mandatory Requirements:**
- **FR-C1**: System MUST escalate to human for pricing/competitor queries. *(Note: Handled by existing backend logic, this refactor MUST NOT break it)*
- **FR-C2**: System MUST escalate messages with sentiment score < 0.3. *(Note: Handled by existing backend logic, this refactor MUST NOT break it)*
- **FR-C4**: All state MUST be persisted in PostgreSQL. *(Note: Handled by existing backend logic)*
- **FR-C5**: All events MUST be processed through Kafka/Redpanda. *(Note: Handled by existing backend logic)*

### Constraints

- **Zero Logic Changes**: The existing `react-hook-form` setup, `zod` validation schema, and `fetch` implementation MUST NOT be modified.
- **Frontend Isolation**: All changes MUST be confined to the `/frontend` directory.
- **Compatibility**: Refactor MUST be compatible with Tailwind CSS v4 and Next.js 14+ App Router.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of interactive elements (buttons, inputs) animate their state changes over a 200ms duration.
- **SC-002**: All form labels and feedback text meet WCAG AA accessibility standards for contrast against the new background and card colors.
- **SC-003**: Form submission functionality remains 100% operational with no changes to the backend integration logic.
- **SC-004**: Support page visual layout remains centered and aesthetically balanced across mobile, tablet, and desktop breakpoints.
