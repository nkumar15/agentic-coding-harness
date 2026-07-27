---
name: feature-architecture
description: Convert an approved PRD into a coding-ready architecture document with implementation order and verification strategy.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "1.0"
---

# Feature Architecture Skill

Produce the technical design that bridges a PRD and implementation.

## Method

1. Read the approved PRD.
2. Read `.agents/rules/project-conventions.md` for stack, source layout, architecture artifact
   location, verification commands, runtime, and hard project rules.
3. Identify data, API, service, UI, integration, migration, config, and deployment impact.
4. Ask questions for unresolved technical ambiguity instead of designing around gaps.
5. Produce a dependency-ordered implementation plan.
6. Map PRD verification requirements to concrete commands, tests, and evidence.

## Required Sections

- Overview
- Inputs and assumptions
- System or module fit
- Data model or persistence impact
- API/interface impact
- Service/business logic
- UI impact, if applicable
- Integration and configuration impact
- Migration or deployment impact, if applicable
- Security and privacy considerations
- Verification strategy
- Implementation order
- Open questions

## Output

Save a Markdown architecture document using the directory and filename convention in
`.agents/rules/project-conventions.md`.
