# Migration Conventions & Project Facts — TEMPLATE

Fill in every `<FILL_IN: ...>` placeholder with your project's values, then copy this file to
`migration-conventions.md`. Delete this header block when you are done.

---

# Migration Conventions & Project Facts

The single home for everything **specific to the `<FILL_IN: project name>` webMethods → Spring Boot
migration**. The capability skills (`java-springboot`, `legacy-code-analysis`,
`junit-parity-testing`) are deliberately generic and know nothing about this project — the agents
bind those generic skills to the facts below. When a skill says "the contract", "the legacy source
root", "the tenant discriminator", etc., the concrete value is here.

---

## Project Bindings

Role files use these terms — fill in each value before starting migration work. All other sections
provide the full detail behind each row.

| Role term | Project value |
|---|---|
| Target API specification | `<FILL_IN: e.g. docs/api/my-api-openapi.json>` |
| Migrated rules directory | `<FILL_IN: e.g. rules/MYAPP/ — or "none" if no rules engine>` |
| Target domain module pattern | `<FILL_IN: e.g. myapp/myapp-{domain}/>` |
| Existing target implementation discovery | `<FILL_IN: how to infer existing/partial target modules for a domain; ask the human if zero or multiple plausible modules remain>` |
| Data access service | `<FILL_IN: e.g. myapp-dal-impl (base path /myapp/db/v1, port 8003) — or "none">` |
| Data access service spec | `<FILL_IN: e.g. docs/api/myapp-dal-openapi.json — or "none">` |
| Live API base URL env var | `<FILL_IN: e.g. MYAPP_API_BASE_URL>` |
| Target Helm charts | `<FILL_IN: e.g. API: helm/myapp-api; DAL/support: helm/myapp-dal — or "none">` |
| Local app health endpoint | `<FILL_IN: e.g. http://127.0.0.1:8080/actuator/health>` |
| Source decision table paths | Market/tenant: `<FILL_IN: e.g. legacy/wm_myapp_impl/framework/rules/*TenantRules/Decision Tables/*.decisiontable>`; shared/common: `<FILL_IN: e.g. legacy/wm_myapp_impl/framework/rules/CommonRules/Decision Tables/*.decisiontable — or "none">` |
| Rule fixture generator | `<FILL_IN: e.g. tools/decision-table-parser/parse_decision_tables.py — or "none">` |
| Rule fixture path pattern | `<FILL_IN: e.g. tests/parity-data/rules/<DecisionTable>/<Market>.json>` |
| Disallowed rule parser | `<FILL_IN: e.g. tools/legacy-rule-export-parser/parse_export.py (reason: stale source) — or "none">` |
| Excluded legacy submodules | `<FILL_IN: e.g. wm_myapp_gateway, wm_myapp_integration — or "none">` |
| Tenant identity field | `<FILL_IN: e.g. x-tenant-id / tenantId — or "none" if single-tenant>` |
| Tenant registry | `<FILL_IN: e.g. REGION_A=1, REGION_B=2 — or "none">` |

Full details for each entry are in the relevant section below.

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Language | `<FILL_IN: e.g. Java 17>` |
| Framework | `<FILL_IN: e.g. Spring Boot 3.2.x>` |
| Rules engine | `<FILL_IN: e.g. plain Java rule classes, or a chosen rules engine — omit row if no rules engine>` |
| Build | `<FILL_IN: e.g. Maven (multi-module under myapp/)>` |
| Data access | `<FILL_IN: e.g. via myapp-dal REST API — never direct JDBC; OR direct JDBC via Spring Data>` |
| HTTP client | `<FILL_IN: e.g. RestTemplate or WebClient>` |
| API docs | `<FILL_IN: e.g. springdoc-openapi annotations>` |
| Testing | `<FILL_IN: e.g. JUnit 5>` |
| Local runtime | `<FILL_IN: local runtime command or wrapper script used by the health gate>` |

## Application Logging

- Logging library/convention: `<FILL_IN: e.g. SLF4J via Spring Boot logging; logger field style if
  mandated by the project>`.
- Log only meaningful operational boundaries: downstream failures, fallback/skip decisions,
  side-effect/write decisions, and rule/branch diagnostics needed for parity or support.
- Do not add method entry/exit noise or duplicate exception logs.
- Never log authorization headers, secrets, full payloads, or personal/health data.

## Target API Specification

`<FILL_IN: path to your OpenAPI/Swagger contract file, e.g. docs/api/my-api-openapi.json>`
(`<FILL_IN: spec format and version, e.g. OpenAPI 3.0, v1.4>`) is the single source of truth for
every endpoint. Every path, param, header, field name, type, and response code must match it
EXACTLY. The contract wins over legacy behavior when they disagree.

- **Required headers** on every endpoint: `<FILL_IN: e.g. Authorization, x-request-id, x-tenant-id>`
  (constants in `<FILL_IN: constants class, e.g. MyAppApiConstants>`:
  `<FILL_IN: constant names, e.g. HEADER_AUTHORIZATION, HEADER_REQUEST_ID, HEADER_TENANT_ID>`).
- **The tenant discriminator** (what the generic skills call "tenant id") is
  `<FILL_IN: header/field that identifies the tenant, e.g. x-tenant-id / tenantId>`.
  Tenant registry:
  `<FILL_IN: e.g. REGION_A=1, REGION_B=2 — or "no multi-tenancy" if single-tenant>`.
- **API base path:** `<FILL_IN: e.g. /myapp/api/v1>` (`<FILL_IN: constant, e.g. MyAppApiConstants.BASE_PATH>`).
- **Param-name constants** live in `<FILL_IN: constants class>` — never inline string literals; they
  must match the contract character-for-character.
- **Authentication scope:** `<FILL_IN: e.g. "No API auth in current scope — Authorization header is
  declared and passed through but not validated." OR "Bearer JWT validated via Spring Security.">`.

## Repository Structure

```
<FILL_IN: new Spring Boot code root, e.g. myapp/>/
  <FILL_IN: app assembly module, e.g. myapp-app/>/        # main app (port <FILL_IN: e.g. 8080>)
  <FILL_IN: shared core module, e.g. myapp-core/>/        # shared DTOs, constants, exceptions
  <FILL_IN: domain module pattern, e.g. myapp-{domain}/>/ # one module per domain/service
  <FILL_IN: rules module if used, e.g. myapp-rule/>/      # rule implementation — omit if no rules engine
<FILL_IN: migrated rules root if used, e.g. rules/MYAPP/>/ # migrated rule assets — omit if none
legacy/                       # READ-ONLY reference — never modify
  <FILL_IN: legacy source path, e.g. wm_myapp_impl/myapp_framework/>/
    <FILL_IN: decision table glob, e.g. rules/**/Decision Tables/*.decisiontable>/
<FILL_IN: contract file path, e.g. docs/api/my-api-openapi.json>/        # the contract
<FILL_IN: DAL spec path if applicable, e.g. docs/api/myapp-dal-openapi.json>/ # omit if no DAL
<FILL_IN: analysis artifacts dir, e.g. .analysis/myapp/>/  # analysis artifacts (gitignored)
```

**Existing target implementation discovery:** for each domain, infer candidate target modules from
the configured domain module pattern, assigned domain name, singular/plural aliases, and contract
package/domain names. If no candidate exists, record the checked paths as `not-found`. If more than
one plausible candidate exists, or the target module name is not derivable from conventions, ask the
human before marking characterization approval-ready.

Existing Spring Boot code, DTOs, DAL clients, tests, or rule assets are current target implementation
evidence only. Characterization must inventory them, compare them with legacy behavior, and hand
explicit `reuse` / `refactor` / `replace` / `defer` / `unknown` decisions to design. Do not assume a
module is complete or behaviorally correct because it exists.

## Module Architecture

Every migration design must lock the target project structure before coding starts. The design
artifact is the approval point; coding agents implement the approved layout, not invent structure
during migration.

- `<FILL_IN: app assembly module>` is the Spring Boot assembly/entrypoint only. No domain logic.
- `<FILL_IN: shared core module>` holds cross-domain constants, shared DTOs, shared config, and
  shared exception shapes only.
- `<FILL_IN: domain module pattern>` owns the public REST controller, domain service, domain DAL
  client, domain DTOs, and field-rename mapping from legacy pipeline names to contract fields.
- `<FILL_IN: rules module if used>` owns reusable rule-engine infrastructure, rule loading/routing,
  and model classes. Domain modules may depend on it; it must not depend on domain modules.
  Omit this bullet if no rules engine.
- Keep dependency direction one-way: app → domain modules → core / rule; rule → core and rule
  assets only.
- Add a new module only when the approved design shows a reusable cross-domain responsibility.
  Do not create per-feature helper modules opportunistically.

## Legacy System Map

**The migration source is `<FILL_IN: legacy source root path>`** — the submodule being migrated.
All legacy submodules are READ-ONLY; their scope:

| Submodule | Role | Scope |
|-----------|------|-------|
| `<FILL_IN: business logic submodule>` | business logic — FlowServices + decision tables | **IN SCOPE** → `<FILL_IN: target>` |
| `<FILL_IN: DAL submodule if applicable>` | DAL | `<FILL_IN: DONE / IN SCOPE / OUT OF SCOPE>` |
| `<FILL_IN: gateway submodule if applicable>` | API Gateway | `<FILL_IN: OUT OF SCOPE / IN SCOPE>` |
| `<FILL_IN: any other submodule>` | `<FILL_IN: role>` | `<FILL_IN: scope>` |

The generic 3-layer flow maps to these concrete packages:
- **Layer 1 (API entry):** `<FILL_IN: legacy entry FlowService path pattern>`
- **Layer 2 (orchestration):** `<FILL_IN: legacy orchestration package>`
- **Layer 3a (rules):** `<FILL_IN: legacy rules call path>` → decision tables under `<FILL_IN: legacy decision table root>`
- **Layer 3b (DB adapters):** `<FILL_IN: legacy DB adapter path>` → now `<FILL_IN: DAL service name>`
- **Layer 3c (connectors if applicable):** `<FILL_IN: connector path>` → `<FILL_IN: target downstream service>`

Decision tables: `<FILL_IN: glob for decision table files per tenant/market, e.g. Tenant{A,B,C}Rules/Decision Tables/*.decisiontable>`
under `<FILL_IN: legacy source root>`.
Shared/common decision tables: `<FILL_IN: glob for non-tenant shared/common decision tables — or "none">`.
Shared/common projects are not tenants/markets; classify them separately when they are required or
transitively required by a migration unit.
`<FILL_IN: any tenant-specific extra tables, e.g. "HK has extra Booster DTs" — or delete this line>`.

## Rule Governance

- **Rule analysis source priority:** authoritative source for characterization is the legacy
  `.decisiontable` files under `<FILL_IN: decision table root glob>`. A human may name an additional
  SME-approved corpus, but the repository migrated rules directory is not such a corpus.
- **Ignore the repository rules directory during analysis inventory.** Do not use migrated rule assets
  to derive source rule counts, fixture rows, market coverage, or parity expectations.
- Migrated rule/model assets are implementation evidence only after they reconcile back to the legacy
  `.decisiontable` source and curated fixtures. They may be wired during migrate only when the
  approved design marks their conversion fidelity as acceptable.
- Generate rule parity fixture candidates from legacy `.decisiontable` files with
  `<FILL_IN: path to decision-table parser tool, e.g. tools/decision-table-parser/parse_decision_tables.py>`.
  The parser emits one JSON file per decision-table/market pair under
  `<FILL_IN: fixture output path, e.g. tests/parity-data/rules/<DecisionTable>/<Market>.json>`,
  plus aggregate summary/count files where applicable. If shared/common rules are required, the
  parser must emit them separately, for example
  `<FILL_IN: e.g. tests/parity-data/rules/common/<DecisionTable>.json>`, without representing common
  as a tenant/market column.
  `<FILL_IN: note any deprecated parser and why — or delete this line>`.
- Keep shared/common rule fixtures distinct from market/tenant fixtures. Do not represent common
  rows as a tenant/market column, and do not let same-named common and market/tenant decision tables
  overwrite each other's fixture files.
- If a required migrated rule asset is missing, document the gap and leave behavior unimplemented
  unless told to fall back.

Rule migration is **`<FILL_IN: migration unit, e.g. domain>`-by-`<FILL_IN: migration unit>`**,
not full-corpus generation. A migration unit must cover every rule table required for that unit
across every applicable tenant/market, including shared/common and transitive tables.

Decision-table classification (use in characterization reports):

| Classification | Meaning | Required handling |
| --- | --- | --- |
| `domain-required` | Directly invoked by the unit's legacy FlowService path. | Must have migrated asset, fixture/parity coverage for every applicable market. |
| `shared-required` | Not directly called but required to interpret outputs or evaluate behavior. | Treat like `domain-required`. |
| `used-by-other-domain` | Belongs to another migration unit and not needed here. | Exclude with source evidence and review note. |
| `not-used-by-this-domain` | Present in the rule project but no source path shows consumption. | Exclude with checked paths and confidence marker. |
| `unknown` | Found but usage cannot be proven or excluded. | Characterize/design blocker until resolved. |
| `excluded-with-approved-reason` | Human-approved exclusion despite possible relevance. | Record approver, date, impact, and follow-up. |

## Data Layer

- DAL: `<FILL_IN: stack, e.g. Spring Boot MyBatis>`, base path `<FILL_IN: e.g. /myapp/db/v1>`,
  port `<FILL_IN: e.g. 8003>`. Inventory in `<FILL_IN: DAL mapping artifact path>`.
- Base URL via `<FILL_IN: env var, e.g. MYAPP_DAL_BASE_URL>`. Other downstream URLs:
  `<FILL_IN: list other env vars, e.g. POLICY_MANAGER_URL, POINTS_MANAGER_URL>` — never hardcode hosts.
- Multi-step ops use `<FILL_IN: atomic endpoint convention, e.g. t-post-* / t-delete-* endpoints>`.

## Parity & Verification

Verification is split into domain-scoped correctness gates plus a baseline-aware cross-domain
regression gate (see `.claude/process/gates.yaml`).

**Golden fixtures live in `<FILL_IN: fixture root, e.g. tests/parity-data/>` (committed — the
verification contract).**

- **Rules parity** (gate `rules_parity_verified`, tag `rules-parity`) — OFFLINE, no app/deploy,
  scoped to the active migration unit.
  Golden rows in
  `<FILL_IN: rules fixture path pattern, e.g. tests/parity-data/rules/<DecisionTable>/<Market>.json>`
  (conditions = inputs, outputs = expected, tenant tag retained in each row). Fixtures derived from
  legacy `.decisiontable` source only. Runs the domain-scoped command declared in
  `gates.rules_parity_verified.checks`.
  The parity verifier writes the gate report to `.analysis/<name>/<name>-rules-parity-report.md`.

- **API parity** (gate `api_parity_verified`, tag `api-parity`) — REMOTE, needs the app **deployed**.
  Fixtures in `<FILL_IN: API fixture path, e.g. tests/parity-data/api/<domain>/<case>.json>`
  (recorded legacy request + expected response). Replayed against the deployed API
  (`<FILL_IN: deployed API env var, e.g. MYAPP_API_BASE_URL>`) and diffed field-by-field, volatile
  fields normalised. Runs the domain-scoped command declared in
  `gates.api_parity_verified.checks`; skipped where the env var is unset (a skip is NOT a pass).
  Failure causes: code-bug / data-drift / fixture-error / conversion-loss / env / missing-rule.
  The parity verifier writes the gate report to `.analysis/<name>/<name>-api-parity-report.md`.

- **Contract conformance** (gate `contract_verified`, tag `contract`) — OFFLINE, scoped to the
  active migration unit. Generate the app's OpenAPI and diff against
  `<FILL_IN: contract file path>`. Runs the domain-scoped command declared in
  `gates.contract_verified.checks`.

- **Domain implementation checks** (gate `domain_migration_checks_green`) — OFFLINE. Run
  domain-scoped build/unit/controller/service/client checks for the active migration unit. Unrelated
  WIP domains must not block this gate.

- **Cross-domain regression** (gate `cross_domain_regression_green`) — OFFLINE. Run the full app
  regression command and prove the active migration unit introduced no new failures. Known WIP
  failures outside the active unit require explicit baseline waivers with baseline branch/commit,
  stable failure signature, owner, expiry/recheck trigger, and current-branch comparison. Compile
  failures, active-unit failures, new failures, changed signatures, and missing baseline evidence
  fail the gate.

- **Spring Boot app health** (gate `springboot_app_health_checked`) — OFFLINE. Start the local
  runtime stack declared by this project and verify the Spring Boot actuator health endpoint
  (`<FILL_IN: local health URL, e.g. http://127.0.0.1:8080/actuator/health>`). This catches
  packaging, Spring context, config binding, rule loading, dependency, and probe issues that Maven
  tests can miss. Record the startup command, health URL/response, service status, and any
  human-approved local-runtime override in the implementation verification report.

- **Manual test** (gate `manual_test_passed`) — MANUAL, requires `deployed_to_environment`. A human
  tester exercises the deployed migration and confirms it behaves as expected. Record the tester,
  scenarios covered, and result in the deploy-and-manual-test phase's change request.

Checkpoint file (engine state, gitignored): `<FILL_IN: e.g. .analysis/myapp/migration-state/<name>.yaml>`.

Artifact paths:
- Characterization: `.analysis/<name>/<name>-characterization.md`
- Architecture: `.analysis/<name>/<name>-migration-architecture.md`
- Progress: `.analysis/<name>/<name>-migration-progress.md`
- Implementation verification: `.analysis/<name>/<name>-implementation-verification-report.md`

## Migration Constraints

1. **Match the contract exactly** — paths, params, headers, field names, types, status codes.
2. **`<FILL_IN: data access constraint, e.g. No direct JDBC — all data via myapp-dal-impl.>`**
3. **Rule source priority** — analyze from legacy `.decisiontable` files; wire only audited
   migrated assets or explicitly approved gaps. Never re-author rules by hand.
4. **No rule fires for the wrong `<FILL_IN: tenant/market>` — zero cross-tenant leakage.** Enforce
   per-rule condition or structurally via per-tenant isolation in the rule implementation. Leakage
   is a critical defect.
5. **Field renames are business logic.** webMethods MAP nodes silently rename fields; reproduce the
   exact output field names the contract promises, in the service layer.
6. **Verification before merge, phase by phase.** No migrate-phase change merges until code review
   passes. No unit-test-phase change merges until domain implementation checks pass. No
   integration-test-phase change merges until contract verification, rules parity, cross-domain
   regression, and local Spring Boot app health all pass. No deploy-and-manual-test-phase change
   merges until deploy, API parity, and manual test all pass. Known WIP failures outside the active
   migration unit require explicit, unchanged baseline waivers; never silently ignore them.
7. **Endpoints thin, logic in services.** Surgical changes only — no refactoring untouched code.
8. **Analyze for real.** Run `legacy-code-analyzer` per `<FILL_IN: migration unit>`.
9. **Strict phase order.** analyze (approved) → design (approved) → migrate (approved) → unit test
   (approved) → integration test (approved) → deploy and manual test (approved). Drive all work
   through `orchestrate`.
10. **No silent decision-table-to-target conversion loss.** Reconcile source rows, fixtures, migrated
    rule logic, and tests before coding. Unresolved conversion-loss items block migration.
11. **Deployment assets stay in sync.** If Spring Boot code changes runtime config, secret
    placeholders, service ports, health endpoints/probes, downstream URLs, ingress/service exposure,
    or container startup assumptions, update the approved Helm chart/values or record an explicit
    deploy-owner gap before review.

## Branch & Commit Conventions

Branch prefixes (extends `scm-conventions.md`):
`docs/<issue>-<name>` (analyze) ·
`migrate/arch-<issue>-<name>` (design) ·
`migrate/dev-<issue>-<name>` (migrate) ·
`migrate/unit-<issue>-<name>` (unit test) ·
`migrate/integration-<issue>-<name>` (integration test) ·
`migrate/deploy-<issue>-<name>` (deploy and manual test).

`<name>` is the kebab-case slug for your migration unit
(`<FILL_IN: list your migration unit names, e.g. peer, ledger, reward, pricing>`).

Commit types: `feat`/`fix`/`test`/`docs`/`refactor`/`chore`.
