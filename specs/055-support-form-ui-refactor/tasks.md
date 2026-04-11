# Tasks: Support Form UI/UX and Animations

**Input**: Design documents from `specs/055-support-form-ui-refactor/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT requested for this purely visual refactor.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/app/`, `frontend/src/components/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency verification

- [x] T001 Verify `lucide-react` is installed in `frontend/package.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared styles that apply across the feature

- [x] T002 [P] Ensure Tailwind v4 is correctly configured in `frontend/package.json`

---

## Phase 3: User Story 1 - Premium Support Page Layout (Priority: P1) 🎯 MVP

**Goal**: Create a professional, centered layout with a subtle background and high-quality typographic header.

**Independent Test**: Navigate to `/support` and verify centered layout with header and subtext.

### Implementation for User Story 1

- [x] T003 [US1] Apply background gradient and centering utilities with `duration-200` transitions in `frontend/app/support/page.tsx`
- [x] T004 [US1] Implement "Contact Customer Success" header and subtext typography in `frontend/app/support/page.tsx`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Modernized Form Interaction (Priority: P1)

**Goal**: Enhance usability through a premium card container, modern input styling, and functional icons.

**Independent Test**: Interact with each form field and observe focus states and icons provide appropriate visual cues.

### Implementation for User Story 2

- [x] T005 [P] [US2] Wrap form in a white card with `shadow-xl` and `rounded-2xl` in `frontend/src/components/SupportForm.tsx`
- [x] T006 [P] [US2] Style input, textarea, and select fields with `rounded-lg`, indigo focus rings, and `duration-200` transitions in `frontend/src/components/SupportForm.tsx`
- [x] T007 [US2] Integrate `lucide-react` icons (User, Mail, MessageSquare) inside input wrappers in `frontend/src/components/SupportForm.tsx`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Interactive Feedback and States (Priority: P2)

**Goal**: Provide clear, elegantly styled feedback for button states and form outcomes.

**Independent Test**: Submit the form and verify button animations and success/error banners.

### Implementation for User Story 3

- [x] T008 [P] [US3] Implement submit button hover, active, and loading spinner states with `duration-200` transitions in `frontend/src/components/SupportForm.tsx`
- [x] T009 [P] [US3] Style success banner (green) and field-level red error text in `frontend/src/components/SupportForm.tsx`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T010 [P] Verify responsiveness and accessibility (check contrast ratios via Chrome DevTools/Lighthouse) in `frontend/app/support/page.tsx` and `frontend/src/components/SupportForm.tsx`
- [x] T011 Run `quickstart.md` validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 but touch different parts of the UI.
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories.
- **User Story 2 (P2)**: No dependencies on other stories.
- **User Story 3 (P3)**: Depends on US2 (inputs/form) for meaningful feedback.

### Parallel Opportunities

- T003 and T005 are in different files and can be worked on in parallel.
- All tasks marked [P] can run in parallel within their respective phases.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Complete Phase 3 (US1).
3. **STOP and VALIDATE**: Verify the basic support page looks professional.

### Incremental Delivery

1. Add US2: Modernize the form interactions and input styling.
2. Add US3: Add the interactive feedback and button animations.
3. Final Polish and verification.
