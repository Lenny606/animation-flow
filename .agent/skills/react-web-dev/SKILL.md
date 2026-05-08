---
name: React Web Development
description: Guidelines and patterns for building React applications with TypeScript, Tailwind CSS, and TanStack Query.
---

# React Web Development Skill

This skill provides a set of instructions and best practices for building modern React applications. It emphasizes simplicity, performance, and a premium aesthetic without relying on 3rd party UI component libraries.

## Core Principles

1. **Simple & Premium UI**: Focus on clean layouts, elegant typography, and subtle micro-animations. Use custom Tailwind styles instead of pre-built component libraries (like Shadcn, MUI, etc.) to maintain full control and minimize bundle size.
2. **Type Safety**: Use TypeScript for all components, hooks, and utilities. Define clear interfaces for props and data models.
3. **Efficient Data Fetching**: Use TanStack Query (React Query) for all server-state management. Avoid storing API data in global state (like Redux or Zustand) unless absolutely necessary.
4. **Vanilla Styling**: Leverage Tailwind CSS for all styling. Use CSS variables for design tokens (colors, spacing, etc.) to ensure consistency.

## Technical Stack

- **Framework**: React (latest)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (Vanilla)
- **Data Management**: TanStack Query (React Query)
- **Router**: React Router or Framework-specific router (e.g., Next.js)

## Implementation Guidelines

### 1. Component Structure
- Use functional components and hooks.
- Keep components small and focused.
- Prefix component files with PascalCase (e.g., `Button.tsx`, `UserCard.tsx`).
- Place components in `src/components`.

### 2. Styling with Tailwind
- Use the predefined design system in `tailwind.config.js`.
- Favor utility classes for layout and spacing.
- Use `clsx` or `tailwind-merge` for conditional classes if needed (though basic template literals are preferred for simplicity).
- Implement dark mode using the `dark:` selector.

### 3. TanStack Query Patterns
- Define custom hooks for all API calls in `src/hooks`.
- centralized `QueryClient` configuration.
- Use `useQuery` for fetching and `useMutation` for updates.
- Always handle `isLoading` and `error` states gracefully.

### 4. TypeScript Best Practices
- Avoid `any`. Use `unknown` if the type is truly unknown.
- Define prop types using `interface`.
- Use discriminated unions for complex state or API responses.

## Resource Files

Check the `resources/` directory for boilerplate configurations:
- [query-client.ts](file:///home/tomas/my-projects/animation-flow/.agent/skills/react-web-dev/resources/query-client.ts) - Standard QueryClient setup.
- [tailwind.config.js](file:///home/tomas/my-projects/animation-flow/.agent/skills/react-web-dev/resources/tailwind.config.js) - Premium theme configuration.
