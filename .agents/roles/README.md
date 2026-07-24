# Role Prompt Standard

Role files define agent behavior and output contracts. They do not own workflow, host wrapping, or
reusable technical capability.

## Layer Boundaries

- `process/` owns phase order, gates, branch shape, and human approval stops.
- `adapters/` bind a role to host metadata and attach skills.
- `skills/` provide reusable technique and capability.
- `rules/` provide durable repository constraints.
- `roles/` define who the agent is, what it owns, how it behaves, what it outputs, and what it must
  not do.

## Recommended Sections

Use this structure unless the role has a strong reason to differ:

```md
# <Role Name>

## Agent Role
The identity and responsibility of this agent.

## Operating Mode
Whether the agent analyzes, designs, implements, verifies, or reviews; whether it may edit files;
and whether it reports only.

## Capability Sources
Skills or rules that provide technique. Reference them; do not duplicate them.

## Inputs Expected
Artifacts and facts this role expects to receive or locate.

## Work Method
Role-specific behavior and ordering.

## Required Output
The artifact, report, code shape, or verdict this role must produce.

## Blocking Conditions
What must be reported instead of guessed.

## Out Of Scope
Work this role must not do.

## Memory Updates
Recurring findings to record.
```

Verifier roles may replace `Required Output` with a fixed report template and add `Routing` for
failure ownership.
