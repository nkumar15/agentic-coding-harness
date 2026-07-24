# <Domain Name> Implementation Verification Report

Status: final migrate-phase implementation/testing evidence for the active domain. The
`springboot-migrator` seeds this report before handoff; verifier agents update it with gate results.

## Summary

| Field | Value |
| --- | --- |
| Domain | `<domain>` |
| Branch | `<branch>` |
| Commit | `<sha>` |
| Architecture | `.analysis/<domain>/<domain>-migration-architecture.md` |
| Progress artifact | `.analysis/<domain>/<domain>-migration-progress.md` |
| Overall verdict | `<PASS / PASS_WITH_BASELINE_WAIVER / FAIL / BLOCKED>` |
| Next required action | `<none / fix / human review / deploy / parity>` |

## Scope Verified

| Scope | Included? | Evidence | Notes |
| --- | --- | --- | --- |
| Active domain module | `<yes/no>` | `<module/tests>` | `<notes>` |
| Required support modules | `<yes/no/n/a>` | `<modules/tests>` | `<rule/core/support rationale>` |
| Contract surface | `<yes/no>` | `<contract command/report>` | `<endpoints>` |
| Downstream contract clients | `<yes/no/n-a>` | `<client tests/source evidence>` | `<SOAP/REST dependencies>` |
| Rules parity | `<yes/no/n/a>` | `<rules parity report>` | `<decision tables/tenants>` |
| Local Spring Boot health | `<yes/no>` | `<local runtime command + health URL/result>` | `<services/probes/runtime override if any>` |
| Helm / deployment impact | `<yes/no/n/a>` | `<chart/value files or no-impact note>` | `<env/secrets/probes/ports/downstream URLs>` |
| API parity readiness | `<yes/no>` | `<fixtures/env notes>` | `<deploy boundary notes>` |
| Cross-domain regression | `<yes/no>` | `<command/result>` | `<new failures?>` |

## Target Code Structure And File Inventory

Record the final implementation shape so reviewers and future agents can quickly see what was added,
modified, or intentionally left untouched.

| Module / Area | Package / Path | New Files | Modified Files | Removed Files | Architecture / WP Reference | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<work-unit-module>` | `<package/path>` | `<files>` | `<files>` | `<files or none>` | `<WP/D-*>` | `<why this belongs here>` |
| `<shared-core-module>` | `<package/path>` | `<files>` | `<files>` | `<files or none>` | `<WP/D-*>` | `<shared DTO/constants rationale>` |
| `<rule-module>` | `<package/path>` | `<files>` | `<files>` | `<files or none>` | `<WP/D-*>` | `<rule facade/routing rationale>` |
| `rules/` | `<path>` | `<files>` | `<files>` | `<files or none>` | `<WP/D-*>` | `<migrated asset verification>` |
| `tests/` | `<path>` | `<fixtures/tests>` | `<fixtures/tests>` | `<files or none>` | `<WP/D-*>` | `<coverage rationale>` |
| `helm/` | `<chart path>` | `<files>` | `<files>` | `<files or none>` | `<WP/D-*>` | `<deployment/runtime impact or no-impact>` |

### Structure Compliance

- Approved target modules touched:
- Dependency direction preserved:
- Domain logic kept out of assembly and shared-core modules:
- DAL access routed only through approved clients:
- Rule assets wired only after verification:
- Existing implementation reused/refactored/replaced as designed:
- Helm/deployment assets updated or explicitly marked no-impact:
- Local runtime health check verified:

## Gate Results

| Gate | Resolved Command | Result | Report / Output | Follow-up |
| --- | --- | --- | --- | --- |
| `domain_migration_checks_green` | `<command>` | `<pass/fail/blocked>` | `<summary>` | `<action>` |
| `contract_verified` | `<command>` | `<pass/fail/blocked>` | `<summary>` | `<action>` |
| `rules_parity_verified` | `<command>` | `<pass/fail/blocked/n-a>` | `.analysis/<domain>/<domain>-rules-parity-report.md` | `<action>` |
| `cross_domain_regression_green` | `<command>` | `<pass/pass-with-baseline-waiver/fail/blocked>` | `<summary>` | `<action>` |
| `springboot_app_health_checked` | `<command(s)>` | `<pass/fail/blocked>` | `<local runtime status + actuator health response>` | `<action>` |
| `migration_review_approved` | `<review verdict>` | `<approve/request-changes/pending>` | `<summary>` | `<action>` |

## Known Baseline Waivers

Use this only for pre-existing WIP failures outside the active domain. A waiver is not allowed for
compile failures, active-domain failures, new failures, changed failure signatures, or missing
evidence.

| ID | Module / Test | Baseline Branch / Commit | Failure Signature | Owner | Expiry / Recheck Trigger | Current Branch Result | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `BW-001` | `<module/test>` | `<branch@sha>` | `<stable error summary>` | `<owner/domain>` | `<date/event>` | `<same/different/not-run>` | `<accepted/rejected>` |

## Domain Test Evidence

| Test Type | Expected Scope | Ran | Passed | Failed | Skipped | Notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Unit | `<controllers/services/clients>` | `0` | `0` | `0` | `0` | `<notes>` |
| Downstream client contract | `<SOAP/REST peer clients>` | `0` | `0` | `0` | `0` | `<namespace/path/schema/request/fault assertions>` |
| Contract | `<domain endpoints>` | `0` | `0` | `0` | `0` | `<notes>` |
| Rules parity | `<tables/tenants or n/a>` | `0` | `0` | `0` | `0` | `<notes>` |
| Local app health smoke | `<local runtime services + health endpoint>` | `0` | `0` | `0` | `0` | `<notes>` |
| API parity fixture readiness | `<recorded cases>` | `0` | `0` | `0` | `0` | `<notes>` |

## Cross-Domain Regression Evidence

- Full command:
- Baseline source:
- New failures introduced: `<yes/no/unknown>`
- Existing known failures unchanged: `<yes/no/n-a>`
- Modules/tests affected:
- Failure classification:
- Remedy / owner:

## Local Spring Boot Health Evidence

- Local runtime:
- Startup command(s):
- Health URL:
- Health response/status:
- Service status:
- Runtime override, if any:
- Failure classification, if failed: `<code/config/packaging/dependency/env/unknown>`
- Remedy / owner:

## Helm / Deployment Evidence

- Chart paths checked:
- Files changed:
- Runtime env/secret/probe/port/downstream URL changes:
- No-impact rationale, if no chart changes:
- Remaining deploy-owner gaps:

## Work Package Completion Evidence

| WP | Status | Implemented Files | Tests / Gates | Open Gaps | Verification Notes |
| --- | --- | --- | --- | --- | --- |
| `WP-001` | `<implemented/verified/blocked>` | `<files>` | `<tests/gates>` | `<gaps>` | `<notes>` |

## Verdict

`<PASS / PASS_WITH_BASELINE_WAIVER / FAIL / BLOCKED>` — `<reason>`.

## Handoff Notes

- What is safe to rely on:
- What remains before deploy boundary:
- What remains before API parity:
- What another agent must read first:
