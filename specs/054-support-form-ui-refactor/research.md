# Research: Support Form UI/UX Refactor

## Tailwind CSS v4 Utilities

### Shadows and Borders
- **Shadow**: `shadow-xl` is standard and provides a soft, premium feel.
- **Rounded Corners**: `rounded-2xl` (1rem) for the main card and `rounded-lg` (0.5rem) for input fields are the requested standards.
- **Focus Rings**: `focus:ring-2 focus:ring-indigo-500 focus:border-transparent` provides a modern, high-contrast focus state.

### Animations and Transitions
- **Utilities**: `transition-all duration-200 ease-in-out` will be applied to all interactive elements (inputs, buttons).
- **Hover/Active**: `hover:scale-[1.01]` and `active:scale-[0.99]` can be used for subtle tactile feedback on buttons.

### Layout Patterns
- **Centered Layout**: `flex items-center justify-center min-h-screen` or a container with `mx-auto` and vertical padding.
- **Backgrounds**: A soft gradient like `bg-gradient-to-br from-gray-50 to-gray-100` or a very light gray `bg-slate-50`.

## Component Architecture

### Icon Integration
- **Pattern**: Wrap inputs in a relative container. Position icons using `absolute left-3 top-1/2 -translate-y-1/2`.
- **Spacing**: Add `pl-10` to the input field when an icon is present.

### Feedback Banners
- **Success**: `bg-green-50 border border-green-200 text-green-800 rounded-lg p-4 flex items-center space-x-3`.
- **Error**: `text-red-600 text-xs mt-1 font-medium`.

## Decisions and Rationale

| Decision | Rationale | Alternatives Considered |
|----------|-----------|-------------------------|
| Relative Icon Positioning | Standard Next.js/Tailwind pattern for input icons; maintains accessibility and layout stability. | Flexbox wrapper (more complex to align perfectly). |
| Indigo Focus Ring | Indigo is a standard "premium" SaaS color; provides clear contrast on white/gray. | Blue (standard but less "premium" feel). |
| Soft Gradient BG | Adds depth without being distracting. | Solid gray (flatter, less modern). |
