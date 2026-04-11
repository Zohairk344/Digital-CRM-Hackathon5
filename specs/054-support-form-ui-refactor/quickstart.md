# Quickstart: Support Form UI Refactor

## Local Development (Frontend)

To run the frontend and verify the UI changes:

1.  Navigate to the `/frontend` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
4.  Navigate to `http://localhost:3000/support` in your browser.

## Testing the Refactor

- **Visual Inspection**: Verify the centered layout, background gradient, and form card styling.
- **Interactive Elements**:
  - Hover over inputs and buttons to see transitions.
  - Click into inputs to see the indigo focus ring.
  - Submit the form with invalid data to see red error highlights.
  - Submit the form with valid data (mock or actual backend) to see the loading spinner and success banner.

## Dependencies

- **Tailwind CSS v4**: Core styling framework.
- **Lucide React**: Icon library.
- **React Hook Form & Zod**: Preserved logic for validation.
