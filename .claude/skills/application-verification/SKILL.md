---
name: application-verification
description: Evaluate feature, bug, chore, docs, and general review gates by running declared checks and reporting results.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "1.0"
---

# Application Verification Skill

Evaluate repository gates without fixing failures.

## Method

1. Read `.claude/process/gates.yaml`.
2. Read `.claude/rules/project-conventions.md`.
3. Resolve command placeholders from project conventions and the active work item.
4. Run every command declared for the gate, even if an earlier command fails.
5. Inspect PRD and architecture verification requirements when evaluating `feature_verification`.
6. Report pass, fail, or blocked with exact commands and actionable failure detail.

## Gate Criteria

- `checks_green` passes only when every resolved global check succeeds.
- `feature_verification` passes only when the feature-specific verification strategy is present,
  implemented, and evidenced.
- Review gates pass only with an approve verdict and no critical or blocking findings.

## Output

Return a concise gate report with:

- gate name
- resolved commands
- pass/fail status per command
- missing or skipped verification
- saved evidence path when the project defines one
- final verdict
