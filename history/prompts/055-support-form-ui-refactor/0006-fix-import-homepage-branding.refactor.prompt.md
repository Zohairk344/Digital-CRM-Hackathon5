---
id: 0006
title: fix-import-homepage-branding
stage: refactor
date: 2026-04-02
---

# PROMPT_TEXT
Fix the Module not found import error for the SupportForm component, and replace the default Next.js boilerplate homepage with a clean, branded entry point.

[ENVIRONMENT & DIRECTORY PROTOCOL]
- Change directory to /frontend before running any commands.
- Use npm for any environment checks.

[EXECUTION PROTOCOL: THE FIX]
1. Locate the Component: Find exactly where SupportForm.tsx was created (e.g., src/components/, components/, or app/components/).
2. Fix the Import: Open app/support/page.tsx (or src/app/support/page.tsx) and correct the import statement on Line 1. Ensure it uses the correct relative path (e.g., import SupportForm from '../../components/SupportForm';) or the @/ alias if configured.

[EXECUTION PROTOCOL: THE HOMEPAGE CLEANUP]
1. Nuke the Boilerplate: Open app/page.tsx (or src/app/page.tsx). Delete all the default Vercel boilerplate code, imports, and images.
2. Build a Clean Landing Page: Write a new, simple Next.js page using Tailwind CSS. 
   - Create a full-screen, centered layout (min-h-screen flex flex-col items-center justify-center bg-gray-50).
   - Add a modern Header (e.g., "Welcome to CRM Digital FTE").
   - Add a clear, styled Next.js <Link> button that says "Go to Support Portal" and routes the user to /support.

[CONSTRAINTS]
- Do NOT alter the internal logic of SupportForm.tsx or the backend API.
- After fixing, run npm run build to verify there are no lingering module resolution errors.

# RESPONSE_TEXT
I have successfully resolved the import error and implemented the branded homepage:
1. **Located SupportForm**: Moved the component from `frontend/app/components/` to `frontend/components/SupportForm.tsx` to align with the suggested path and standard Next.js conventions.
2. **Fixed Import**: Updated `frontend/app/support/page.tsx` with the correct relative import: `import SupportForm from '../../components/SupportForm';`.
3. **Homepage Cleanup**: Replaced the Next.js boilerplate in `frontend/app/page.tsx` with a clean, centered landing page using Tailwind CSS, branded for "CRM Digital FTE," and including a link to the support portal.
4. **Metadata Update**: Updated `frontend/app/layout.tsx` to include professional CRM Digital FTE titles and descriptions.
5. **Validation**: Verified the fix by running `npm run build`, which compiled successfully without module resolution errors.
