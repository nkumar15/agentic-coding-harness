# BMAD Comparison

This note explains how this portable agentic coding harness differs from the BMAD Method and how
to position both clearly with development teams.

## Short Positioning

BMAD is a broad AI-native agile development framework with guided workflows, specialized agents,
modules, and an installer-driven ecosystem. This repository is intentionally lighter: a repo-native
workflow package focused on helping Codex and Claude Code assist existing development teams through
project conventions, explicit gates, reusable roles, and human approval points.

The two approaches are not mutually exclusive. BMAD is useful when a team wants a comprehensive
AI-native planning and delivery framework. This package is useful when a team wants a small,
auditable workflow layer that fits into an existing repository and engineering governance model.

## Comparison

| Area | BMAD Method | Portable Agentic Coding Harness |
|---|---|---|
| Primary intent | Broad AI-driven agile development framework from ideation and planning through implementation. | Lightweight, repo-native workflow for consistent AI assistance in existing engineering repositories. |
| Adoption model | Install a framework/ecosystem, commonly through `npx bmad-method install`. | Copy the workflow package, fill convention files, regenerate `.claude/` and `.codex/agents/`, then validate. |
| Scope | Broad lifecycle support, modules, specialized agents, guided planning, and extension mechanisms. | Focused processes for feature, bug, chore, and docs workflows. |
| Best fit | Teams that want a comprehensive AI-native agile method and are comfortable adopting a framework. | Teams that already have engineering practices and want agents to work inside existing repo standards. |
| Context model | Builds context progressively through generated planning artifacts and project context. | Keeps mutable project facts in `.agents/rules/project-conventions.md`. |
| Governance model | Structured workflows and agents guide the lifecycle. | Explicit process gates, verifier/reviewer roles, human approvals, and CI portability validation. |
| Host support | Supports multiple AI coding assistants that can consume custom prompts/context. | Generates first-class adapters for Codex and Claude Code from one `.agents/` source tree. |
| Stack support | General and extensible through BMAD modules and customization. | Concrete reusable skills for Python/FastAPI, Java/Spring Boot, React, PostgreSQL, pytest, and JUnit. |
| Human role | Human collaboration is part of guided workflows. | Human engineering judgment, testing standards, code review decisions, and approval gates remain authoritative. |

## How To Explain It To Teams

Use this framing:

> BMAD is a comprehensive AI-native agile framework. Our portable agentic coding harness is a
> lighter repo-native package designed to fit into existing engineering teams. It standardizes how
> Codex and Claude assist with implementation, verification, and review work while keeping project
> conventions and human approval gates central.

The practical reason for this package is internal reuse: a repeatable pattern for guiding agents
through requirements, design, implementation, verification, and review so teams can adopt it for
day-to-day feature work, bug fixes, chores, and documentation.

## When To Use Which

Use BMAD when:

- the team wants a broader AI-native agile framework
- ideation, research, planning, UX, architecture, and story generation need end-to-end framework
  support
- the team wants to adopt BMAD's ecosystem, installer, agents, and modules

Use this workflow package when:

- the team wants a lightweight process layer inside an existing repository
- project-specific engineering conventions already exist or can be documented
- human review, verification evidence, approval gates, and governance need to stay explicit
- Codex and Claude Code should share the same source workflow definitions

## Sources

- [BMAD Method docs overview](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/index.md)
- [BMAD Method GitHub README](https://github.com/bmad-code-org/bmad-method)
- [BMAD workflow map](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/workflow-map.md)
- [BMAD official modules](https://docs.bmad-method.org/reference/modules/)
