---
id: 001
title: Finalize support form UI specification
stage: spec
date: 2026-03-31
surface: agent
model: gemini-2.0-pro
feature: support-form-ui-refactor
branch: 053-support-form-ui-refactor
user: zohai
command: /sp.specify [arguments]
labels: ["spec", "ui-refactor", "support-form"]
links:
  spec: specs/053-support-form-ui-refactor/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/053-support-form-ui-refactor/spec.md
  - specs/053-support-form-ui-refactor/checklists/requirements.md
tests:
  - N/A
---

## Prompt

[CONTEXT] Build "Feature 2.1: Support Form UI/UX and Animations". The functional logic for the Next.js Support Form (Feature 2.2) is already implemented and working perfectly using `react-hook-form`, `zod`, and native `fetch`. The objective of this feature is strictly to refactor the visual presentation to match a premium, modern SaaS application aesthetic. [TECH STACK] - Framework: Next.js 14+ (App Router) - Styling: Tailwind CSS v4 - Icons: `lucide-react` - Package Manager: `npm` (Frontend only) [UI/UX REQUIREMENTS] 1. **Page Layout (`app/support/page.tsx`):** - Create a professional, centered layout with a subtle background (e.g., a very light gray or a soft gradient). - Add a high-quality typographic header (e.g., "Contact Customer Success") and a brief, welcoming subtext. 2. **Form Card (`SupportForm.tsx`):** - Wrap the form in a clean white card container with soft shadows (`shadow-xl`), rounded corners (`rounded-2xl`), and spacious padding. 3. **Input Fields & Typography:** - Style all inputs, textareas, and select dropdowns with modern borders, rounded corners (`rounded-lg`), and clear, distinct focus states (e.g., a blue or indigo focus ring). - Use crisp, accessible typography for labels (small, medium-weight, dark gray). - Integrate `lucide-react` icons inside or adjacent to the input fields to provide visual cues (e.g., a User icon for Name, Mail icon for Email). 4. **Interactive States & Animations (Tailwind Native):** - **Buttons:** The submit button must have clear hover state transitions, active (click) states, and a disabled state that reduces opacity and shows a spinning loading icon when submitting. - **Feedback:** Success messages should appear as distinct, elegantly styled banners (e.g., soft green background with dark green text and a check icon). Error states on individual fields must be clearly highlighted in red with accompanying small red text. - **Transitions:** Use Tailwind's `transition-all duration-200` utilities to ensure all hover effects and focus rings animate smoothly rather than snapping instantly. [CONSTRAINTS & SAFEGUARDS] - **Zero Logic Changes:** You MUST NOT alter the existing `react-hook-form` implementation, the `zod` schema, or the asynchronous `fetch` logic that communicates with the FastAPI backend. - **Frontend Isolation:** This feature is strictly confined to the `/frontend` directory. Do not propose any changes to the backend.

## Response snapshot

The specification for `053-support-form-ui-refactor` is already initialized and verified, matching the user's input exactly. No updates were required as the current `spec.md` and `checklists/requirements.md` are complete and pass all validation criteria.

## Outcome

- ✅ Impact: Finalized specification and verified readiness for planning.
- 🧪 Tests: No tests run as this was a specification turn.
- 📁 Files: specs/053-support-form-ui-refactor/spec.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The spec was already perfectly aligned with the user's request, so I verified its integrity rather than reinventing it.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
