# Claude And Codex Agentic Workflow Design

This package makes one workflow source usable from both Claude Code and Codex.

## Design Goal

Keep workflow intent in one shared source tree and keep host execution details at the edges.

The shared workflow answers:

- Which processes exist?
- Which phases and gates must run?
- Which role owns each phase or gate?
- Which skills define reusable technique?
- Which provider operation represents tracking and code review?

The host adapters answer:

- How is the role exposed to Claude Code or Codex?
- Which model, tools, memory mode, and metadata are used?
- Which generated file format does the host discover?

## Architecture

```text
AGENTS.md                      # Codex entrypoint
CLAUDE.md                      # Claude Code entrypoint

.agents/                       # canonical shared workflow source
  rules/
  process/
  skills/
  roles/
  adapters/
    claude/
    codex/

.claude/                       # generated Claude adapter output
  agents/
  skills/
  process/
  rules/

.codex/
  agents/                      # generated Codex custom-agent wrappers

scripts/
  generate-agent-adapters.py
  validate-agent-portability.py
```

Humans edit `.agents/`; generated host output is committed for fresh-clone behavior.

## Supported Processes

| Process | Shape | Primary roles |
|---|---|---|
| `feature` | PRD -> architecture -> development | `prd-writer`, `architect`, `full-stack-developer` |
| `bug` | reproduce -> fix -> test | `full-stack-developer` |
| `chore` | describe -> implement | `full-stack-developer` |
| `docs` | write -> review | inline or docs author |
| `migration` | analyze -> design -> migrate -> unit test -> integration test -> deploy and manual test | `legacy-code-analyzer`, `microservice-target-architect`, `springboot-migrator` |

Reviewer and verifier roles are modeled as gates so they can enforce quality without becoming new
artifact-producing phases.

Detailed workflow design, rationale, gates, and convention requirements are documented in
workflow-specific README files:

- [Feature workflow](feature/README.md)
- [Bug workflow](bug/README.md)
- [Chore workflow](chore/README.md)
- [Docs workflow](docs/README.md)
- [Migration workflow](migration/README.md)

## Generator Contract

The generator is deterministic and safe to run repeatedly. It generates:

```text
.agents/roles/*.md + .agents/adapters/claude/*.yaml -> .claude/agents/*.md
.agents/roles/*.md + .agents/adapters/codex/*.yaml  -> .codex/agents/*.toml
.agents/skills/*                                   -> .claude/skills/*
.agents/process/*                                  -> .claude/process/*
.agents/rules/*                                    -> .claude/rules/*
```

It does not generate or overwrite Claude-local memory/settings.

## Validator Contract

The validator fails when canonical source and generated output drift. It also checks that:

- required files and directories exist
- every role has Claude and Codex adapter metadata
- every adapter-declared skill exists
- every role-declared skill is included in adapter metadata
- every process phase references existing roles
- every process gate reference exists
- canonical rules/process/roles/skills do not reference generated host paths
- the selected provider has a provider file

## Adoption Recipe

1. Copy this package into a target repo.
2. Fill `.agents/rules/project-conventions.md`.
3. Fill `.agents/rules/migration-conventions.md` if a migration is in scope.
4. Replace placeholder gate commands in `.agents/process/gates.yaml` with convention-backed
   commands.
5. Regenerate adapters and validate.
6. Restart Claude Code or Codex if needed so new wrappers are discovered.

## Common Mistakes

- Editing generated `.claude/` or `.codex/agents/` output directly.
- Putting project paths or commands in role files.
- Copying Claude memory from another repo without review.
- Treating an artifact file as proof that a phase ran.
- Letting README skill or role lists drift from the filesystem.
