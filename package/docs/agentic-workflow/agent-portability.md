# Agent Portability

This repository keeps shared agentic workflow instructions in one canonical source tree and
generates host-specific adapter files for Claude Code and Codex.

## Source Of Truth

Edit shared workflow content under `.agents/`:

- `.agents/rules/` for project, SCM, command, verification, and behavior conventions.
- `.agents/process/` for feature, bug, chore, docs, gates, and provider specs.
- `.agents/skills/` for reusable skill packages.
- `.agents/roles/` for host-neutral role behavior.
- `.agents/adapters/claude/` for Claude role metadata.
- `.agents/adapters/codex/` for Codex role metadata.

## Generated Outputs

Do not edit generated outputs directly.

- `.claude/agents/` is generated from `.agents/roles/` plus `.agents/adapters/claude/`.
- `.claude/skills/`, `.claude/process/`, and `.claude/rules/` are generated copies for Claude
  discovery compatibility, with canonical `.agents/` references rewritten to `.claude/`.
- `.codex/agents/` is generated from `.agents/roles/` plus `.agents/adapters/codex/`.

Claude-local files such as `.claude/agent-memory/`, `.claude/settings.json`, and
`.claude/settings.local.json` are not canonical workflow source.

## Importing External Skills

To pull an external skill package (e.g. from `npx skills add`-compatible sources) into canonical
source, use:

```bash
python3 scripts/add-skill.py <owner>/<repo> --skill <skill-name>
```

This wraps `npx skills add ... -a universal --copy`, which installs directly to
`.agents/skills/<skill-name>/` — never into generated `.claude/skills/`. It only fetches skill
content; it does not wire the skill into any role's `skills:` list. After importing, add the skill
name to the relevant `skills:` entries in `.agents/adapters/{claude,codex}/*.yaml`, then regenerate
and validate (below). The validator fails if an imported skill is never referenced by an adapter or
entrypoint file.

## Regeneration

Run this after changing shared workflow source or adapter metadata:

```bash
python3 scripts/generate-agent-adapters.py
python3 scripts/validate-agent-portability.py
git diff --exit-code
```

The validator checks required files, dynamic role/adapter coverage, declared skill coverage,
unreferenced (unwired) skills, generated output drift, process role references, process gate
references, provider selection, and host-neutral canonical files.

## Host Boundaries

`AGENTS.md` is the Codex runtime entrypoint.

`CLAUDE.md` is the Claude Code runtime entrypoint.

Shared project conventions belong in `.agents/rules/`, not in generated host policy locations.

## Workflow Details

Detailed operating guides live in workflow-specific README files:

- [Feature workflow](feature/README.md)
- [Bug workflow](bug/README.md)
- [Chore workflow](chore/README.md)
- [Docs workflow](docs/README.md)

## Project-Specific Boundary

Only convention files should contain project facts:

- `.agents/rules/project-conventions.md`

Everything else should refer back to those files for paths, commands, work-unit names, source roots,
domain lists, deployment environments, and environment variables.
