# Migration Implementation Checklist

Use this checklist during the migrate phase after the architecture is approved. The approved
`.analysis/<domain>/<domain>-migration-architecture.md` is the source of truth; do not expand scope
from legacy source during coding unless a blocker routes back to analyze/design.

## Before Coding

- [ ] Confirm the current phase is migrate and the design approval gate has passed.
- [ ] Read the approved architecture and list all `WP-*` work packages.
- [ ] Read the architecture handoff sections: Characterization Intake Map, Open Question
      Disposition, Existing Implementation Reuse / Remediation Plan, Design Decisions, Design Gaps
      And Blockers, Rule Asset Gap And Remediation Plan, and Scenario To Test Traceability.
- [ ] Confirm every `WP-*` has target files/classes, dependencies, acceptance criteria, and tests.
- [ ] For each active `WP-*`, record linked architecture `D-*` decisions, linked `G-*`
      gaps/blockers, related characterized scenarios, required tests/gates, and dependent work
      packages in the progress artifact before editing code.
- [ ] Confirm no work package depends on unresolved characterization or design gaps.
- [ ] Confirm no active work package depends on an unresolved characterization `Q-*` or an
      unresolved `G-*` unless the architecture records a human-approved design assumption.
- [ ] Confirm rule assets to be wired have conversion-fidelity evidence, implementation-shape
      verification, and market coverage.
- [ ] Confirm every rule-dependent functional `WP-*` is ordered after any required Rule Asset Gap
      And Remediation Plan work package.
- [ ] Confirm every existing implementation item in scope is classified as `reuse`, `refactor`,
      `replace`, `defer`, or `unknown`; dependent work is blocked when classification is `unknown`.
- [ ] Confirm target project structure, module ownership, and dependency direction are locked.
- [ ] Confirm every functional config/reference-data dependency in the active `WP-*` has an
      approved target source, owner, default/fallback behavior, secret handling, and test
      obligation.
- [ ] Confirm every SOAP/REST peer dependency in the active `WP-*` has approved downstream contract
      evidence: endpoint config, protocol, namespace/localPart or method/path, schemaVersion/action,
      request/response/fault mapping, and test obligation.
- [ ] Confirm every active `WP-*` has an approved deployment/runtime impact decision: Helm chart
      changes required, no Helm impact, or explicit deploy-owner gap. Check env vars, secret-backed
      values, ports, probes, health endpoints, downstream URLs, and startup/profile behavior.
- [ ] Confirm the project-declared local runtime and `springboot_app_health_checked` gate command
      are understood before changing code that can affect startup, packaging, config, or rule
      loading.
- [ ] Create or update `.analysis/<domain>/<domain>-migration-progress.md` from
      `templates/migration-progress-template.md`.
- [ ] Create or update `.analysis/<domain>/<domain>-implementation-verification-report.md` from
      `templates/implementation-verification-report-template.md` before handing the implementation
      to verifier/reviewer agents.

## Per Work Package

- [ ] Implement only the approved target files/classes for the `WP-*`.
- [ ] Keep the `WP-*` trace current: linked `D-*`, linked `G-*`, scenarios, tests/gates, target
      files/classes, blockers, and next action.
- [ ] Preserve contract path, method, headers, params, field names, types, and status codes exactly.
- [ ] Keep controllers thin; put orchestration, pipeline mapping, and field renames in services.
- [ ] Implement architecture decisions exactly. Do not substitute an easier behavior when a `D-*`
      decision or scenario trace says otherwise.
- [ ] Respect design gaps. If implementation reaches a `G-*` blocker, stop and route it instead of
      coding around it.
- [ ] Use DAL clients for downstream data/API access; do not call JDBC or peer services directly.
- [ ] Propagate legal entity, request id, and authorization headers as required by design.
- [ ] Implement timeout/retry/failure mapping only as approved by design or documented project
      convention.
- [ ] Implement downstream SOAP/REST clients from approved contract evidence. Do not guess SOAP
      namespace, root localPart, schemaVersion, SOAPAction, REST method, path, or request/response
      shape from ad-hoc examples.
- [ ] Implement functional config/reference-data behavior through the approved target source only.
      Do not hardcode values from legacy runtime config files unless the design explicitly approved
      them as static reference data.
- [ ] Update Helm charts, base values, environment overlays, and secret-placeholder files when the
      `WP-*` changes runtime config, secrets, service ports, probes, downstream URLs, or deployment
      behavior. Never commit real secrets.
- [ ] Preserve side-effect order, atomic write boundary, idempotency, and partial-failure behavior in
      scope.
- [ ] Add logging only where the approved design, source evidence, dependency behavior, or project
      convention justifies it. Use standard SLF4J/Spring Boot application logging, avoid method
      entry/exit noise, avoid duplicate exception logs, and never log secrets, tokens,
      request/response bodies, or personal/health data.
- [ ] Wire only audited rule assets with implementation-shape verification and preserve market
      isolation.
- [ ] Complete required rule-asset remediation work before functional code that depends on those
      rules; do not replace missing rules with hardcoded constants, partial market shortcuts, or DAL
      snapshots unless the approved architecture explicitly permits that gap.
- [ ] If existing implementation is classified `reuse`, add regression/parity tests that prove the
      reuse is valid. If it is `refactor` or `replace`, remove or change stale reachable behavior.
- [ ] Add or update unit tests in the same pass as implementation.
- [ ] Add or update contract, rules parity, or API parity tests/fixtures when the `WP-*` affects
      those surfaces.
- [ ] For every characterized scenario linked to the `WP-*`, add a unit, contract, rules parity,
      API parity, or explicitly approved gap entry before marking the `WP-*` complete.
- [ ] Update the progress artifact with status, files, tests, gaps, blockers, and review notes.
- [ ] Update the Resume Cursor so the next agent knows the exact next action, next file, next
      command, expected result, and stop condition.

## Local Verification Before Gate Agents

- [ ] No unresolved `WP-*` marked complete without tests or an approved reason.
- [ ] No completed `WP-*` is missing architecture `D-*`/`G-*` traceability in the progress artifact.
- [ ] No completed `WP-*` is missing scenario-to-test traceability or an approved design gap.
- [ ] No implementation preserves stale existing-target behavior that architecture marked
      `refactor` or `replace`.
- [ ] No work package bypasses a required Rule Asset Gap And Remediation Plan item.
- [ ] No silent skipped tests, missing fixtures, or partial market/rule coverage.
- [ ] No hardcoded hosts, secrets, market ids outside approved constants/config, or direct database
      calls.
- [ ] SOAP/REST client tests assert exact endpoint config, namespace/localPart or method/path,
      schemaVersion/action, request fields, response mapping, and fault/error mapping for every
      touched peer dependency.
- [ ] No behavior-affecting legacy config value is copied into code without an approved static
      reference-data decision; config-driven branches and defaults have tests.
- [ ] No required Helm/deployment update is omitted: new/changed env vars, secret placeholders,
      ports, health probes, service exposure, and downstream URLs are reflected in the approved
      chart/values files or recorded as an explicit deploy-owner gap.
- [ ] No new logs expose secrets, authorization headers, full payloads, or personal/health data; any
      new logs use safe context such as operation, request id, tenant/legal entity, and dependency
      name only when approved for logging.
- [ ] No rule asset with unresolved conversion-loss evidence is wired.
- [ ] `domain_migration_checks_green`, `contract_verified`, `rules_parity_verified`, and
      `cross_domain_regression_green` are ready to be evaluated by their gate agents.
- [ ] `springboot_app_health_checked` is ready to run: the local runtime stack can build/start, the
      API health endpoint is known, and startup/config/packaging defects have been fixed or routed.
- [ ] Any cross-domain WIP failure needed for the full regression gate is recorded as a specific
      Known Cross-Domain Baseline Waiver with baseline branch/commit, stable failure signature,
      owner, expiry/recheck trigger, and current-branch comparison status.
- [ ] API parity prerequisites are documented for the deploy boundary, including the required live
      API base URL env var from migration conventions and fixture/data-state assumptions.

## Progress Artifact Minimum

Use `templates/migration-progress-template.md`; do not invent a different shape.

For each approved `WP-*`, record:

| Field | Meaning |
| --- | --- |
| `status` | `not-started`, `in-progress`, `implemented`, `verified`, `blocked`, or `deferred-approved` |
| `architecture decisions/gaps` | Linked `D-*` decisions and `G-*` gaps/blockers from the architecture |
| `scenario/test trace` | Characterized scenarios and the unit/contract/rules/API parity tests or approved gaps that cover them |
| `depends on` | Prior `WP-*`, rule remediation, human decision, or gate prerequisite |
| `implemented files` | Files/classes changed for the work package |
| `tests` | Unit, contract, rules parity, API parity, or manual checks affected |
| `open gaps` | Known incomplete behavior with owner/phase |
| `blockers` | Issues that prevent gate progression |
| `review notes` | Notes for verifier/reviewer/human SME |

Also include:

- resume cursor: current branch, commit, worktree state, active `WP-*`, exact next action, next
  files, next command, expected result, and stop condition;
- last known good state: last green commit, last completed work package, last passing checks, and
  offline checkpoint if any;
- cross-LLM handoff summary: what is done, in progress, must not be redone, risks, and next steps;
- source artifacts and report links;
- implementation verification report link and current verdict;
- local Spring Boot app health-check result, command, URL, local runtime, and any approved override;
- Helm/deployment impact status and chart/value files changed or explicitly not required;
- decisions made and open decisions;
- do-not-redo / do-not-change notes;
- files changed since last checkpoint;
- verification history;
- parity state;
- blockers and routing by cause/owner.
