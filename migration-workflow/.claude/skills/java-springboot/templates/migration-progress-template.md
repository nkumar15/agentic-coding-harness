# <Domain Name> Migration Progress

Status: migrate-phase working memory and handoff artifact. Keep this current after every meaningful
implementation checkpoint, before stopping work, before human review, and after any gate result.

## Resume Cursor

This is the first section a future Codex, Claude, or human should read.

- Current branch:
- Current commit:
- Worktree state when last updated: `<clean/dirty and summary>`
- Current phase/gate:
- Active work package:
- Exact next action:
- Next file(s) to open:
- Next command to run:
- Expected result of next command:
- Stop condition:

## Last Known Good State

| Item | Value |
| --- | --- |
| Last green commit | `<sha or none>` |
| Last completed `WP-*` | `<id>` |
| Last passing build/check | `<command/result/date>` |
| Last passing contract gate | `<command/result/date>` |
| Last passing rules parity gate | `<command/result/date/report>` |
| Last passing local app health gate | `<command/result/date or none>` |
| Last passing API parity gate | `<command/result/date/report>` |
| Offline checkpoint | `<none or project-declared migration-state checkpoint path with commit>` |

## Cross-LLM Handoff Summary

Write this as plain operational context for another agent that has not seen the conversation.

- Goal:
- Scope:
- What is already done:
- What is currently in progress:
- What must not be redone:
- Most important constraints:
- Known risks:
- Recommended next 3 steps:

## Source Artifacts

| Artifact | Path | Status | Notes |
| --- | --- | --- | --- |
| Characterization | `.analysis/<domain>/<domain>-characterization.md` | `<approved/stale/gap>` | `<notes>` |
| Architecture | `.analysis/<domain>/<domain>-migration-architecture.md` | `<approved/stale/gap>` | `<notes>` |
| Progress | `.analysis/<domain>/<domain>-migration-progress.md` | `<current/stale>` | `<notes>` |
| Implementation verification report | `.analysis/<domain>/<domain>-implementation-verification-report.md` | `<pass/pass-with-baseline-waiver/fail/blocked/missing>` | `<notes>` |
| Rules parity report | `.analysis/<domain>/<domain>-rules-parity-report.md` | `<pass/fail/blocked/missing>` | `<notes>` |
| API parity report | `.analysis/<domain>/<domain>-api-parity-report.md` | `<pass/fail/blocked/missing>` | `<notes>` |

## Architecture Handoff State

Record how the approved architecture is being consumed during implementation. This prevents the
migrate phase from dropping decisions, gaps, scenarios, or rule-remediation dependencies.

| Architecture Section | Implementation Status | Notes / Gaps |
| --- | --- | --- |
| Characterization Intake Map | `<consumed/partial/gap>` | `<notes>` |
| Open Question Disposition | `<all resolved / accepted gaps / blocker>` | `<Q-* to D-* / G-* mapping>` |
| Existing Implementation Reuse / Remediation Plan | `<consumed/partial/gap>` | `<reuse/refactor/replace/defer/unknown notes>` |
| Rule Asset Gap And Remediation Plan | `<not-applicable / pending / in-progress / complete / blocker>` | `<rule asset dependencies>` |
| Scenario To Test Traceability | `<pending / in-progress / complete / blocker>` | `<coverage notes>` |
| Design Decisions | `<consumed/partial/gap>` | `<D-* notes>` |
| Design Gaps And Blockers | `<none / accepted / blocking>` | `<G-* notes>` |

## Work Package Board

| WP | Status | Owner | Scope | Architecture Decisions / Gaps | Scenario / Test Trace | Depends On | Implemented Files | Tests | Open Gaps | Blockers | Review Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `WP-001` | `<not-started/in-progress/implemented/verified/blocked/deferred-approved>` | `<agent/human>` | `<scope>` | `<D-* / G-*>` | `<scenario -> test/gate>` | `<WP/rule remediation/human/gate>` | `<files>` | `<tests>` | `<gaps>` | `<blockers>` | `<notes>` |

## Scenario To Test Ledger

Every characterized scenario touched by an implemented work package must have a test obligation or
an approved design gap.

| Scenario | Source / Architecture Reference | Related WP | Test Type | Test / Fixture | Status | Gap / Blocker |
| --- | --- | --- | --- | --- | --- | --- |
| `<scenario>` | `<characterization section / architecture row>` | `<WP>` | `<unit/contract/rules parity/API parity/edge>` | `<test or fixture path>` | `<pending/pass/fail/gap>` | `<none or G-*>` |

## Rule Asset Remediation Ledger

Use this when the architecture has source decision tables/fixtures but missing or unverified target
rule assets. Functional rule-dependent work packages must depend on completed remediation rows.

| Rule Asset Gap | Tables / tenants | Required Asset / Class / Test | Related WP | Status | Evidence | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| `<gap>` | `<tables/tenants>` | `<rule-impl/model/routing/parity/isolation>` | `<WP>` | `<pending/in-progress/complete/blocked>` | `<compile/load/test/report>` | `<WP or behavior>` |

## Runtime / Helm / Health State

Record runtime and deployment state for resume. This prevents a future agent from treating Maven
success as proof the service can actually start.

| Area | Status | Evidence | Owner / Next Action |
| --- | --- | --- | --- |
| Local runtime health | `<pass/fail/blocked/not-run>` | `<command + health URL/result>` | `<owner/action>` |
| Helm chart impact | `<updated/no-impact/gap/not-checked>` | `<chart/value files or rationale>` | `<owner/action>` |
| New/changed env vars | `<none/list/gap>` | `<properties + values files>` | `<owner/action>` |
| Secret placeholders | `<none/updated/gap>` | `<values-env-secrets or secret owner>` | `<owner/action>` |
| Health probes | `<unchanged/updated/gap>` | `<probe paths and actuator exposure>` | `<owner/action>` |

## Current Active Thread

- Active files:
- Current code path:
- Current failing/pending test:
- Current unanswered implementation question:
- Partial work not yet safe to rely on:

## Decisions Made

| ID | Decision | Source / Rationale | Impact | Revisit Trigger |
| --- | --- | --- | --- | --- |
| `D-001` | `<decision>` | `<architecture/source/human>` | `<impact>` | `<when to revisit>` |

## Design Gaps Accepted Or Blocking

| ID | Gap / Blocker | Status | Affected WP | Impact | Owner / Route | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| `G-001` | `<gap>` | `<accepted/blocking/resolved>` | `<WP>` | `<impact>` | `<owner>` | `<action>` |

## Open Decisions / Human Questions

| ID | Question | Impact | Options | Recommendation | Owner | Needed Before |
| --- | --- | --- | --- | --- | --- | --- |
| `Q-001` | `<question>` | `<impact>` | `<options>` | `<recommendation>` | `<owner>` | `<phase/gate/WP>` |

## Do Not Redo / Do Not Change

- `<completed or approved item that should not be reworked unless evidence changes>`

## Files Changed Since Last Checkpoint

| File | Change Summary | Related WP | Test Coverage | Notes |
| --- | --- | --- | --- | --- |
| `<path>` | `<summary>` | `<WP>` | `<test>` | `<notes>` |

## Verification History

Keep latest result first. Preserve failures that explain current work.

| Date / Commit | Command or Gate | Result | Report / Output | Follow-up |
| --- | --- | --- | --- | --- |
| `<date/sha>` | `<command/gate>` | `<pass/fail/blocked/skipped>` | `<report path or summary>` | `<next action>` |

## Known Cross-Domain Baseline Waivers

Use only for pre-existing WIP failures outside the active domain. Waivers must be specific and
auditable; they are not allowed for compile failures, active-domain failures, new failures, changed
failure signatures, or missing baseline evidence.

| ID | Module / Test | Baseline Branch / Commit | Failure Signature | Owner | Expiry / Recheck Trigger | Current Status |
| --- | --- | --- | --- | --- | --- | --- |
| `BW-001` | `<module/test>` | `<branch@sha>` | `<stable error summary>` | `<owner/domain>` | `<date/event>` | `<same/different/resolved>` |

## Parity State

### Rules Parity

- Required tenants:
- Required decision tables:
- Fixture status:
- Conversion-fidelity status:
- Latest report:
- Current verdict:
- Gaps/blockers:

### API Parity

- Fixture status:
- Data-state assumptions:
- Deployed endpoint:
- Latest report:
- Current verdict:
- Gaps/blockers:

## Blockers And Routing

| Blocker | Cause Type | Owner / Route | Impact | Required Action |
| --- | --- | --- | --- | --- |
| `<blocker>` | `<code-bug/data-drift/fixture-error/conversion-loss/env/config/missing-rule-impl/design-gap/human-decision>` | `<owner>` | `<impact>` | `<action>` |

## Next-Session Checklist

- [ ] Confirm branch and worktree state match Resume Cursor.
- [ ] Read approved architecture and this progress artifact before editing.
- [ ] Do not redo completed `WP-*` items unless verification evidence changed.
- [ ] Start with the Exact next action from Resume Cursor.
- [ ] Update this artifact before stopping or after any gate result.
