---
id: 0005
title: Fix Import Error and Home Cleanup
stage: red
date: 2026-04-01
surface: agent
model: gemini-cli
feature: 055-support-form-ui-refactor
branch: 055-support-form-ui-refactor
user: zohai
command: /sp.implement
labels: ["fix", "cleanup", "nextjs", "import-error"]
links:
  spec: specs/055-support-form-ui-refactor/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/app/support/page.tsx
 - frontend/app/page.tsx
tests:
 - npm run build
---

## Prompt

[OBJECTIVE]
Fix the `Module not found` import error for the SupportForm component, and replace the default Next.js boilerplate homepage with a clean, branded entry point.

[ENVIRONMENT & DIRECTORY PROTOCOL]
- Change directory to `/frontend` before running any commands.
- Use `npm` for any environment checks.

[EXECUTION PROTOCOL: THE FIX]
1. **Locate the Component:** Find exactly where `SupportForm.tsx` was created (e.g., `src/components/`, `components/`, or `app/components/`).
2. **Fix the Import:** Open `app/support/page.tsx` (or `src/app/support/page.tsx`) and correct the import statement on Line 1. Ensure it uses the correct relative path (e.g., `import SupportForm from '../../components/SupportForm';`) or the `@/` alias if configured.

[EXECUTION PROTOCOL: THE HOMEPAGE CLEANUP]
1. **Nuke the Boilerplate:** Open `app/page.tsx` (or `src/app/page.tsx`). Delete all the default Vercel boilerplate code, imports, and images.
2. **Build a Clean Landing Page:** Write a new, simple Next.js page using Tailwind CSS. 
   - Create a full-screen, centered layout (`min-h-screen flex flex-col items-center justify-center bg-gray-50`).
   - Add a modern Header (e.g., "Welcome to CRM Digital FTE").
   - Add a clear, styled Next.js `<Link>` button that says "Go to Support Portal" and routes the user to `/support`.

[CONSTRAINTS]
- Do NOT alter the internal logic of `SupportForm.tsx` or the backend API.
- After fixing, run `npm run build` to verify there are no lingering module resolution errors.

## Response snapshot

I identified that `SupportForm.tsx` was located in `frontend/app/components/`, while `app/support/page.tsx` was attempting to import it from a non-existent `src/components/` directory. I corrected the import path to `../components/SupportForm`. Additionally, I replaced the default Next.js homepage boilerplate in `app/page.tsx` with a clean, branded landing page featuring a centered card and a link to the support portal. Verified the fixes with a successful `npm run build`.

## Outcome

- ✅ Impact: High - Resolved module resolution errors and provided a professional entry point.
- 🧪 Tests: PASSED (Build successful).
- 📁 Files: Updated app/support/page.tsx and app/page.tsx.
- 🔁 Next prompts: None.
- 🧠 Reflection: Verifying file locations recursively is essential when multiple directory structures (like 'app' and 'src') coexist in a Next.js project.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
