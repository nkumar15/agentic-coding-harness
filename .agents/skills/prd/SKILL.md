---
name: prd
description: Produce a Product Requirements Document for a feature. Use during the feature PRD phase before architecture or implementation.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "2.0"
---

# PRD Skill

Create clear, actionable Product Requirements Documents for feature work.

## Method

1. Read `.agents/rules/project-conventions.md` for PRD location, naming, product context, and
   verification expectations.
2. Ask only essential clarifying questions when the request is ambiguous.
3. Write requirements in a way a developer or AI agent can implement without guessing.
4. Save the PRD to the project-defined PRD location.

## Required Sections

- Overview
- Goals
- Non-goals
- Users or personas
- User stories with acceptance criteria
- Functional requirements
- Technical or integration considerations
- Verification requirements
- Open questions

## Verification Requirements

Every PRD must state the confidence needed before merge:

- user-visible acceptance checks
- unit, integration, contract, migration, seed, UI, or smoke coverage as applicable
- local commands or command groups from project conventions
- fixture or test-data expectations
- explicit non-goals for verification artifacts that belong to separate work

## Output

Save a Markdown PRD using the directory and filename convention in
`.agents/rules/project-conventions.md`.
