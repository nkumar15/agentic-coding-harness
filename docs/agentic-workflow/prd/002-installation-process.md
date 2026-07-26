# PRD: Installation Process For Adopting This Package

- Issue: #2
- Status: Draft
- Phase: prd

## Overview

Today, adopting this package means manually copying `.agents/`, `.claude/`, `.codex/agents/`,
`AGENTS.md`, `CLAUDE.md`, `scripts/`, and `docs/agentic-workflow/` into a target repository, then
hand-filling `.agents/rules/project-conventions.md` and `.agents/process/gates.yaml` (root
`README.md#how-to-use-this`). There is no scripted install, no update path, and no way to layer an
optional add-on (such as the extracted `migration-workflow` package) onto an already-adopted repo.

This PRD defines a scripted installation process: a one-line `curl` command (POSIX shell, for
macOS/Linux) and an equivalent one-line Windows command (PowerShell), both invoking an installer that
copies the package into the target repository and interactively prompts for initial configuration
instead of leaving `project-conventions.md` fully manual.

## Goals

- Replace "copy this package into the target repository" with a single documented command per
  platform.
- Have the installer interactively collect enough answers (process provider, stack skills, source/
  test roots, PRD/architecture directories, verification commands) to write a first-pass
  `project-conventions.md` and `config.yaml`, rather than leaving every field as `<FILL_IN>`.
- Support re-running the installer against an already-adopted repository to pick up upstream changes
  without clobbering a filled-in `project-conventions.md` or customized `gates.yaml` commands.
- Provide a mechanism for installing an optional add-on package (e.g. `migration-workflow`) on top of
  an already-installed base package.

## Non-Goals

- Redesigning the phases/gates/roles/skills model itself.
- Building the `migration-workflow` add-on's own packaging (tracked separately once it has its own
  repository).
- A package-manager-grade dependency/version resolver.
- A GUI installer.
- CI coverage of the Windows path in this iteration (see Open Questions).

## Users

- A developer or team adopting this workflow package into an existing, already-populated repository.
- A developer on Windows without a POSIX shell available.
- A team that already adopted the package and wants to pull in later improvements.
- A team that wants to add the optional `migration-workflow` add-on after already running the base
  install.

## User Stories

1. As a developer adopting this workflow, I run one `curl` command in my repo and get a working
   `.agents/`, `.claude/`, `.codex/agents/`, `AGENTS.md`, `CLAUDE.md`, `scripts/`, and
   `docs/agentic-workflow/` without manually copying files.
2. As a Windows developer, I run one equivalent PowerShell command and get the same result.
3. As an adopter, the installer asks me a short set of configuration questions (process provider,
   stack skills, source/test roots, PRD/architecture directories, verification commands) and uses my
   answers to pre-fill `project-conventions.md` and `config.yaml`, instead of handing me an all-
   placeholder file.
4. As a team that already adopted the package, I re-run the installer and it updates the generic
   package files (`.agents/`, `.claude/`, `.codex/agents/`, `scripts/`) while leaving my filled
   `project-conventions.md` and customized `gates.yaml` commands untouched, reporting anything it
   could not safely merge.
5. As a team that wants the migration-workflow add-on, I run a documented add-on install command
   against a repo that already has the base package, without re-deriving directory layout
   conventions from scratch.

## Functional Requirements

1. A published one-line command for macOS/Linux (`curl -fsSL <install-url> | sh`) installs the
   package into the current repository.
2. A published one-line command for Windows (PowerShell, e.g. `irm <install-url> | iex`) does the
   same.
3. The installer copies exactly the shipped path set: `.agents/`, `.claude/`, `.codex/agents/`,
   `AGENTS.md`, `CLAUDE.md`, `scripts/`, `docs/agentic-workflow/`.
4. The installer detects an existing install (e.g. `.agents/` already present) and switches to update
   mode instead of blind overwrite.
5. In update mode, the installer never silently overwrites an already-filled
   `.agents/rules/project-conventions.md` or a `.agents/process/gates.yaml` whose commands no longer
   match the shipped placeholders; it reports the conflict instead of guessing.
6. On first install, the installer interactively prompts for: process provider (`local`/`github`),
   backend/frontend/test stack skills, application source root, test root, PRD directory, feature
   architecture directory, verification evidence location, and global verification commands — then
   writes the answers into `project-conventions.md` and `config.yaml`.
7. After copying or updating, the installer runs `scripts/generate-agent-adapters.py` and
   `scripts/validate-agent-portability.py` and reports failures clearly before exiting.
8. A documented, separate add-on install command layers an optional add-on package (starting with
   `migration-workflow`) onto a repo that already has the base package installed.
9. Root `README.md#how-to-use-this` is rewritten to lead with the new install commands instead of
   "Copy this package into the target repository."

## Technical Considerations

- The `curl`/PowerShell one-liners should point at a stable reference (e.g. `main` or a tagged
  release), not an unpinned moving target, so re-runs are reproducible.
- The POSIX installer should be plain `sh` (not bash-only) for portability; the Windows installer
  should run on stock PowerShell without extra modules.
- Copy/update logic must be idempotent and safe by default: never destroy an adopter's existing
  customizations without an explicit confirmation or a `--force`-style flag.
- Exact fetch mechanism (self-contained script vs. script-that-clones) and hosting location are open
  — see Open Questions.

## Verification Requirements

- User-visible acceptance checks:
  - Running the macOS/Linux command against a clean, empty git repo produces a working
    `.agents/`, `.claude/`, `.codex/agents/`, `AGENTS.md`, `CLAUDE.md`, `scripts/`, and
    `docs/agentic-workflow/` tree, and `scripts/validate-agent-portability.py` passes.
  - Running the Windows command against a clean, empty git repo produces the same result.
  - Re-running either installer against a repo with an already-filled `project-conventions.md` and a
    customized `gates.yaml` leaves both files unchanged and reports what it skipped.
  - The interactive prompts, when answered, produce a `project-conventions.md` with no remaining
    `<FILL_IN>` placeholders for the fields asked.
- Expected coverage: a scripted smoke test harness exercising (a) fresh install and (b) update-
  without-clobber, run against scratch temporary git repositories; a manual smoke pass on Windows
  PowerShell since Windows CI is out of scope for this iteration.
- Local commands a developer should run: invoke the installer against a scratch temp repo, confirm
  exit code 0 and expected files present, then run `python3 scripts/validate-agent-portability.py`.
- Test data/fixtures: a scratch empty-repo fixture (fresh install path) and a scratch repo fixture
  pre-seeded with a filled `project-conventions.md` and edited `gates.yaml` (update path).
- Explicit non-goals: no installer performance benchmarking; no Windows CI job in this iteration
  (tracked as an open question below, not assumed done).

## Open Questions

1. Where is the installer script hosted for `curl`/`irm` to fetch — a raw file on `main`, or a
   versioned GitHub Release asset? This affects update/reproducibility semantics.
2. Should the installer be a single self-contained script, or a small bootstrap script that then
   clones/downloads the rest of the package?
3. Should Windows support be PowerShell-only, or also ship a `.cmd`/`.bat` wrapper for `cmd.exe`
   users who won't run `irm`?
4. How does the add-on install mechanism locate an add-on like `migration-workflow` once it lives in
   its own separate repository — a second `curl`/`irm` command pointed at that repo, or a flag on the
   base installer?
