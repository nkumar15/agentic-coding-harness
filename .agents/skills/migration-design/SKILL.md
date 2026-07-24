---
name: migration-design
description: Convert an approved legacy characterization into a coding-agent-ready migration architecture — target project structure, traceability, DTO/DAL/rule/error mappings, work packages, and test/parity plan. Use during the design phase of a legacy-to-Spring-Boot migration.
license: Proprietary
metadata:
  author: Neeraj
  version: "1.0"
---

# Migration Design

Use this skill in the design phase after characterization is approved. The design artifact converts
legacy behavior into target implementation decisions. It must be concrete enough that the coding
agent can implement without re-reading legacy source or inventing module boundaries.

## Canonical Template

Use `templates/migration-architecture-template.md` for every domain design artifact. Produce:

`.analysis/<domain>/<domain>-migration-architecture.md`

Do not copy an older domain artifact as the source of structure. Domain artifacts may contain stale
decisions; the skill template is the reusable output contract.

## Design Rules

- Start only from an approved characterization with resolved open questions or explicit design
  gaps.
- Preserve the API contract exactly: paths, methods, headers, params, field names, types, and
  response codes.
- Lock target project structure before coding starts: Maven modules, packages/classes, dependency
  direction, rule-asset routing, DTO ownership, and shared-core additions.
- Include C4-style architecture views so human reviewers and coding agents can see boundaries
  before implementation: System Context, Container, and Component diagrams. Keep diagrams concrete
  to the domain, tied to characterized dependencies, and consistent with the approved target project
  structure. Use text-based Mermaid diagrams unless the repository establishes another diagram
  format.
- Consume any characterization section that inventories existing or partial target implementation.
  Do not assume existing Spring Boot code, DTOs, tests, DAL clients, or rule assets are correct.
  Classify each existing item as `reuse`, `refactor`, `replace`, `defer`, or `unknown`, and create
  remediation work packages before coding stories that depend on it.
- Carry service signatures, pipeline lineage, field-mapping-step renames, branch logic, dependency
  behavior, side effects, atomic write boundaries, functional config/reference-data findings, and the complete
  characterized error-code inventory into explicit target decisions. Do not reduce error handling
  to directly hardcoded domain codes; preserve direct, dependency-propagated, shared/common
  translation, unused, and unknown-reachability classifications.
- For every characterized SOAP/REST peer dependency, preserve the exact downstream wire contract:
  runtime endpoint config source, protocol, REST method/path or SOAP namespace/localPart,
  schemaVersion/SOAPAction when applicable, request/response/fault mapping, propagated
  headers/auth, and client contract test obligations. Do not let coding agents infer namespace,
  root element, schemaVersion, method, or path from examples when WSDL/XSD/source evidence exists.
- For every behavior-affecting config/reference lookup characterized, decide the target source:
  Spring configuration property, secret-backed property, application config, DAL/reference-data
  endpoint, committed test fixture, static reference value approved by design, or explicit gap.
  Preserve key construction, env/tenant/market variance, defaults/fallbacks, and failure behavior.
  Do not let coding agents copy legacy config file values into constants unless the design
  explicitly approves that as static reference data.
- State deployment/runtime impact for each target change: local runtime needs, Helm chart/value
  updates, environment variables, secret placeholders, service ports, actuator health paths,
  liveness/readiness probes, ingress/service exposure, and deploy-owner gaps. If there is no impact,
  say so explicitly.
- Design may wire only rule assets with acceptable decision-table-to-target conversion-fidelity
  evidence from legacy decision-table artifacts. Repository `rules/` assets are migrated
  implementation output, not source evidence; if they already exist, design must verify they follow
  the migration process before wiring: compile/load or build success, module/package routing, model
  compatibility, fixture/test reconciliation, and market isolation. Stale/non-authoritative
  evidence is not acceptable unless a human explicitly approved a named exception.
- Create `WP-*` work packages that are independently implementable and include files/classes,
  dependencies, acceptance criteria, tests/gates, and open gaps.
- Map characterization evidence to design decisions and then to code/test obligations.
- Treat missing markets, unresolved conversion loss, unavailable rule assets, unresolved DAL
  mappings, and unresolved side effects as blockers or explicit human-approved design gaps.

## Characterization Intake Rules

Before producing target design decisions, create a characterization intake map. The map must show
where each characterization section is consumed in the architecture artifact:

- Open Questions / Decisions Required -> Design Decisions or Design Gaps And Blockers.
- Existing / Partial Target Implementation Baseline -> Existing Implementation Reuse /
  Remediation Plan and related `WP-*` work packages.
- Functional Scenarios And Edge Cases -> Test And Parity Plan and work-package tests.
- Pipeline Variable Lineage and Field-Mapping Renames -> Service Orchestration, DTO mapping, and
  code/test traceability.
- Dependency Behavior Register -> target config, headers/auth, timeout/retry, and failure mapping.
- Downstream Contract Evidence -> exact client contract, runtime URL/config ownership, request and
  response mapping, fault mapping, and client contract tests.
- Functional Config And Reference Data -> target configuration source, secret handling,
  env/tenant/market variance, defaults/fallbacks, failure behavior, and code/test obligations.
- Error Codes And Messages -> Error Handling, exception mapper, response body/status mapping, and
  direct/propagated/shared/unused/unknown test obligations.
- Side Effects And Atomic Write Boundaries -> atomic write strategy, idempotency, duplicate guards,
  and partial-failure behavior.
- Rule Corpus, Required Rule Asset Coverage, Golden Fixtures, and Conversion Fidelity Audit ->
  Rules Design, rule remediation work packages, and rules parity tests.

No orphan questions are allowed. Every `Q-*` from characterization must become exactly one of:

- a resolved `D-*` design decision;
- a `G-*` design blocker/gap;
- an explicit human-approved design assumption, with owner and required follow-up phase.

No orphan scenarios are allowed. Every characterized happy path, edge case, negative case,
dependency-failure case, side-effect case, and market-isolation case must appear in the test plan or
in a documented design gap.

No orphan existing implementation is allowed. Every existing controller, service, DTO, DAL client,
test, rule asset, config, or module found by characterization must be classified as `reuse`,
`refactor`, `replace`, `defer`, or `unknown`. `replace` and `refactor` decisions need remediation
work packages; `unknown` blocks dependent coding work.

When characterization has source decision tables and fixtures but no acceptable rule asset, the
design must create remediation work packages before any story wires rule-dependent behavior. Those
work packages must cover asset generation or authoring, model classes, market routing,
compile/load evidence, fixture reconciliation, rules parity tests, and market isolation.

## Required Handoffs

The design artifact must hand off:

- target controller methods, DTOs, services, DAL clients, rule facades/assets, config/env keys, and
  complete error handling;
- explicit target decisions for functional config/reference data, including source, ownership,
  secret treatment, refresh/caching assumptions when relevant, defaults/fallbacks, and tests;
- exact downstream contract decisions for SOAP/REST peer dependencies, including WSDL/XSD/source
  evidence, endpoint configuration ownership, request/response/fault mapping, and tests;
- existing implementation reuse/refactor/replace decisions, when current target code exists;
- a characterization intake map that proves each major characterization section was consumed;
- C4 System Context, Container, and Component diagrams that identify external systems, target
  runtime/deployable containers, module/component ownership, dependency direction, and trust/data
  boundaries;
- deployment/runtime and Helm chart impact decisions that tell the coding agent which chart/value
  files to update, which health endpoint must pass locally, and which deploy gaps remain;
- a no-orphan-question disposition for every `Q-*`;
- `Characterization -> Design -> Code/Test` traceability;
- implementation order and `WP-*` work packages;
- unit, contract, rules parity, API parity, and edge/negative test plan;
- remediation work packages before any story that wires a suspect rule asset;
- human review checklist and remaining design blockers.
