# Implementation Plan: Support Form UI/UX Refactor

**Branch**: `054-support-form-ui-refactor` | **Date**: 2026-04-01 | **Spec**: [specs/054-support-form-ui-refactor/spec.md]

## Summary

This plan outlines the visual refactor of the support form to achieve a premium, modern SaaS aesthetic using Tailwind CSS v4 and `lucide-react`. The primary goal is to enhance the layout, form card, input fields, and interactive states without modifying the underlying `react-hook-form` and `zod` logic.

## Technical Context

**Language/Version**: TypeScript 5.x, Next.js 14+ (App Router)
**Primary Dependencies**: Tailwind CSS v4, `lucide-react`, `react-hook-form`, `zod`
**Storage**: N/A (Frontend refactor only; uses existing FastAPI backend)
**Testing**: Manual visual validation via `npm run dev` and form interaction testing.
**Target Platform**: Web (Desktop, Tablet, Mobile)
**Project Type**: Next.js Web Application
**Performance Goals**: Instant hover and focus state transitions (200ms duration).
**Constraints**: Zero changes to existing data-handling logic or backend integrations.
**Scale/Scope**: Refactor restricted to `app/support/page.tsx` and `SupportForm.tsx`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Role & Autonomy**: Architect role assumed for UI/UX refactor.
- [x] **II. Technical Stack Sovereignty**: Next.js and Tailwind CSS v4 are being utilized.
- [x] **III. Architectural Standards**: Monorepo structure maintained; frontend changes only.
- [x] **IV. Business Logic Constraints**: N/A (Logic preserved).
- [x] **V. Coding Style & Safety**: Strict TypeScript and Tailwind v4 standards applied.
- [x] **VI. Operational Procedure**: Refactor of Web Support Form is prioritized.

## Project Structure

### Documentation (this feature)

```text
specs/054-support-form-ui-refactor/
├── plan.md              # This file
├── research.md          # UI patterns and Tailwind v4 research
├── data-model.md        # Existing form data structure
├── quickstart.md        # Dev server and testing instructions
└── contracts/
    └── api.md           # Existing POST webhook contract
```

### Source Code (repository root)

```text
frontend/
├── app/
│   └── support/
│       └── page.tsx      # Target: Layout and header refactor
└── src/
    └── components/
        └── SupportForm.tsx # Target: Form card, inputs, and feedback refactor
```

## Step-by-Step Implementation Logic

### Step A: Page Layout Refactor (`app/support/page.tsx`)
1.  Apply a subtle background (very light gray or soft gradient) to the main container.
2.  Center the content both horizontally and vertically using flexbox utilities.
3.  Add a high-quality typographic header ("Contact Customer Success") and a brief, welcoming subtext with modern spacing.

### Step B: Form Card Styling (`SupportForm.tsx`)
1.  Wrap the existing form in a white card container with `shadow-xl`, `rounded-2xl`, and generous internal padding.
2.  Set the max-width to ensure an elegant profile on larger screens.

### Step C: Modernized Input Fields
1.  Update all input, textarea, and select elements with:
    - `rounded-lg` corners.
    - Modern borders (e.g., `border-slate-200`).
    - Clear indigo/blue focus rings with `focus:ring-2`.
    - `transition-all duration-200` for smooth state changes.
2.  Integrate `lucide-react` icons (User, Mail, MessageSquare) inside a relative wrapper for each input, ensuring appropriate padding (`pl-10`).

### Step D: Enhanced Interactive States
1.  Refactor the submit button with:
    - Smooth hover transitions.
    - Tactile active (click) states (e.g., `active:scale-[0.98]`).
    - A clear disabled state that reduces opacity.
    - A spinning `Loader2` icon visible during the `loading` state.

### Step E: Polished Feedback UI
1.  Success State: Style the success message as an elegant banner with a soft green background, dark green text, and a check icon.
2.  Error States: Ensure field-level validation errors are highlighted in red with small, accessible error text appearing below the input.

## Validation Strategy

1.  **Visual Verification**: Run `npm run dev` and navigate to `/support`. Compare the implementation against the SaaS aesthetic requirements.
2.  **Interaction Testing**:
    - Verify all hover and focus states animate smoothly (200ms).
    - Trigger validation errors to verify field-level red highlights.
    - Perform a successful submission to verify the loading spinner and success banner.
3.  **Cross-Device Check**: Confirm the layout and card sizing remain responsive across mobile and desktop.

## Complexity Tracking

> **No Constitution violations detected.**
