---
name: application-implementation
description: Implement application changes from an approved design using project conventions and in-pass tests.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "1.0"
---

# Application Implementation Skill

Implement feature, bug, chore, and documentation work using the consuming repository's conventions.

## Method

1. Read `.claude/rules/project-conventions.md`.
2. For feature work, read the approved PRD and architecture before editing.
3. For bug work, reproduce or characterize the defect before fixing it.
4. Keep changes scoped to the requested work and the active process phase.
5. Write or update tests in the same pass as code.
6. Run the commands declared by the process gates after resolving placeholders from conventions.
7. Record verification evidence in the project-defined location.

## Implementation Rules

- Match the existing codebase patterns.
- Do not invent stack conventions outside project conventions.
- Do not silently deviate from approved architecture.
- Do not add speculative abstractions.
- Do not leave changed behavior without focused verification.

## Output

Produce the code, tests, documentation, or configuration changes required by the active process
phase, plus verification evidence.
