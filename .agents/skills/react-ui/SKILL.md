---
name: react-ui
description: Implement React UI changes using the component, routing, API, state, styling, and design-system conventions declared by the consuming repository.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "2.0"
---

# React UI Skill

Use this skill only when `.agents/rules/project-conventions.md` says the project uses React.
Project conventions define JavaScript versus TypeScript, routing, component layout, API client,
state library, design system, styling approach, and build/test commands.

## Components

- Match the repository's component style: function components, file naming, props conventions, and
  colocated tests/styles when applicable.
- Keep route/page components responsible for composition and data loading.
- Keep reusable components focused on rendering and local interaction.
- Add loading, empty, error, and permission states for data-backed UI.

## API And State

- Use the project-defined API client and data-fetching library.
- Do not issue raw network calls from components when the project has API hooks or service modules.
- Keep server state, URL state, and local UI state separate.
- Preserve cache invalidation and optimistic-update rules declared by project conventions.

## Styling And Design System

- Use project-defined tokens, theme variables, component library, and layout primitives.
- Do not hardcode brand colors, typography, spacing, radius, or shadows when tokens exist.
- Avoid adding a second styling system unless project conventions approve it.
- Keep text and controls responsive without overlap or layout shift.

## Accessibility

- Use semantic elements where possible.
- Ensure forms have labels, errors are announced or visible, and keyboard flow is preserved.
- Do not rely on color alone to communicate state.

## Verification

- Run the project-defined UI build, lint, unit, interaction, or smoke checks from gates/conventions.
- Add focused tests for changed behavior when the repository has UI test infrastructure.
- Confirm changed screens handle loading, error, empty, and success states.
