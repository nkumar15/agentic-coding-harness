---
name: orchestrate
description: Drive a tracked work item through its declared process, enforcing gates and delegating each phase to the declared role. Use when starting, advancing, or resuming feature, bug, chore, docs, or migration work.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "4.0"
---

# SDLC Orchestration Engine

This skill drives work through the process declared under `.claude/process/`. It knows how to load
the declarations, identify the next phase, enforce gates, and delegate work. It does not own project
facts, concrete commands, or host-specific launch mechanics.

## Inputs

| Input | File | Purpose |
|---|---|---|
| Config | `.claude/process/config.yaml` | Selects the active provider adapter. |
| Process spec | `.claude/process/<type>.yaml` | Defines phases, branch patterns, artifacts, and gates. |
| Gates | `.claude/process/gates.yaml` | Defines gate meaning, gate agents, commands, manual stops, and routing. |
| Provider | `.claude/process/provider.<provider>.yaml` | Maps abstract tracker/VCS operations to concrete commands or manual operations. |
| Project conventions | `.claude/rules/project-conventions.md` | Supplies application-specific facts for feature, bug, chore, and docs work. |
| Migration conventions | `.claude/rules/migration-conventions.md` | Supplies migration-specific facts for migration work. |

## Provider Operations

The engine uses abstract operations. The active provider maps them to concrete commands or manual
instructions:

| Op | Purpose |
|---|---|
| `find_ticket` | Locate an existing work item. |
| `create_ticket` | Create a work item with type and priority. |
| `set_phase` | Mark the active phase. |
| `open_change_request` | Open or describe the review request for the phase. |
| `change_request_merged` | Confirm human approval or merge. |
| `mark_done` | Mark the work item complete. |

## Execution Model

1. Read `.claude/process/config.yaml`, the selected process spec, `.claude/process/gates.yaml`, and
   `.claude/process/provider.<provider>.yaml`.
2. Resolve the work item. Search first; create only when the user asked to start new tracked work
   and no duplicate exists. Ask for missing priority when the active provider requires it.
3. Determine the next phase from the process spec, existing phase markers, and human approval gate
   state. Do not infer phase completion from an artifact file alone.
4. Run exactly one phase per invocation:
   - Check the phase `entry_gate`.
   - Set the phase marker through the provider.
   - Create or switch to the phase branch pattern.
   - Delegate the phase to its declared `agent`, or perform the phase inline when no agent is
     declared.
   - Evaluate the phase `exit_gate`.
5. Stop at every human or manual gate. Resume on the next invocation after the user confirms the
   gate has passed.
6. After the final phase's final human gate passes, run the provider `mark_done` operation.

## Gate Vocabulary

| Gate form | Meaning |
|---|---|
| `none` | Always passes. |
| `change_request_merged` | Current phase review is approved or merged by a human. |
| `change_request_merged:<phase>` | A named prior phase review is approved or merged by a human. |
| agent gate | A gate in `gates.yaml` with `agent` and optional `checks`; delegate it and route failures to `on_fail`. |
| manual gate | A gate in `gates.yaml` with `manual: true`; stop for external confirmation. |
| gate with `requires` | Evaluate only after the prerequisite gate has passed. |
| `all_of` | Evaluate each listed gate in order and stop at the first blocker. |

Gate failures are hard stops. Do not skip, downgrade, or work around a failed gate.

## Migration Resume Checkpoint

Migration processes may include expensive offline gates followed by a manual deploy boundary. If the
active process or migration conventions define a checkpoint path, write a checkpoint after all
offline gates pass and before the manual deploy gate. Record:

- work-unit name
- branch
- gate verdicts
- reviewer or approver for review gates
- `checkpoint_commit`
- next gate

On resume, trust the checkpoint only when `HEAD` still matches `checkpoint_commit`; otherwise rerun
the offline gates.

## Extending

- Add a lifecycle by creating `.claude/process/<type>.yaml`.
- Add a gate by editing `.claude/process/gates.yaml`.
- Add a provider by creating `.claude/process/provider.<provider>.yaml` and selecting it in
  `.claude/process/config.yaml`.
- Add a role under `.claude/roles/` and adapter metadata under `.claude/adapters/`.

## Hard Rules

1. Do not start a phase before its entry gate passes.
2. Do not run more than one process phase in one invocation.
3. Do not continue past a human or manual gate.
4. Do not hardcode project paths, commands, domains, URLs, or environment names in this skill.
5. Do not edit generated host adapter files directly.
