---
id: 0001
title: Generate Support Form Refactor Spec
stage: spec
date: 2026-04-01
surface: agent
model: gemini-cli
feature: 054-support-form-ui-refactor
branch: 054-support-form-ui-refactor
user: zohai
command: /sp.specify
labels: ["spec", "ui-refactor", "support-form"]
links:
  spec: specs/054-support-form-ui-refactor/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/054-support-form-ui-refactor/spec.md
 - specs/054-support-form-ui-refactor/checklists/requirements.md
tests:
 - N/A
---

## Prompt

Build "Feature 2.1: Support Form UI/UX and Animations". The functional logic for the Next.js Support Form (Feature 2.2) is already implemented and working perfectly using `react-hook-form`, `zod`, and native `fetch`. The objective of this feature is strictly to refactor the visual presentation to match a premium, modern SaaS application aesthetic. [TECH STACK] - Framework: Next.js 14+ (App Router) - Styling: Tailwind CSS v4 - Icons: `lucide-react` - Package Manager: `npm` (Frontend only) [UI/UX REQUIREMENTS] 1. **Page Layout (`app/support/page.tsx`):** - Create a professional, centered layout with a subtle background (e.g., a very light gray or a soft gradient). - Add a high-quality typographic header (e.g., "Contact Customer Success") and a brief, welcoming subtext. 2. **Form Card (`SupportForm.tsx`):** - Wrap the form in a clean white card container with soft shadows (`shadow-xl`), rounded corners (`rounded-2xl`), and spacious padding. 3. **Input Fields & Typography:** - Style all inputs, textareas, and select dropdowns with modern borders, rounded corners (`rounded-lg`), and clear, distinct focus states (e.g., a blue or indigo focus ring). - Use crisp, accessible typography for labels (small, medium-weight, dark gray). - Integrate `lucide-react` icons inside or adjacent to the input fields to provide visual cues (e.g., a User icon for Name, Mail icon for Email). 4. **Interactive States & Animations (Tailwind Native):** - **Buttons:** The submit button must have clear hover state transitions, active (click) states, and a disabled state that reduces opacity and shows a spinning loading icon when submitting. - **Feedback:** Success messages should appear as distinct, elegantly styled banners (e.g., soft green background with dark green text and a check icon). Error states on individual fields must be clearly highlighted in red with accompanying small red text. - **Transitions:** Use Tailwind's `transition-all duration-200` utilities to ensure all hover effects and focus rings animate smoothly rather than snapping instantly. [CONSTRAINTS & SAFEGUARDS] - **Zero Logic Changes:** You MUST NOT alter the existing `react-hook-form` implementation, the `zod` schema, or the asynchronous `fetch` logic that communicates with the FastAPI backend. - **Frontend Isolation:** This feature is strictly confined to the `/frontend` directory. Do not propose any changes to the backend.

## Response snapshot

I have generated the feature specification for the Support Form UI/UX and Animations. The specification defines functional requirements for the premium layout, form card, input fields, and interactive states, all while strictly adhering to the zero-logic-change constraint.

## Outcome

- ✅ Impact: High - Provides a professional UI/UX for the support channel.
- 🧪 Tests: No tests run yet; spec defines acceptance scenarios.
- 📁 Files: Generated spec.md and requirements checklist.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The user's input was very detailed, allowing for a comprehensive spec with minimal clarifications needed.

## Evaluation notes (flywheel)

- Failure modes observed: Initial PHR creation had path issues due to bash/windows path differences.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
