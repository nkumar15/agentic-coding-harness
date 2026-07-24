---
name: legacy-code-analysis
description: Read and understand a legacy source system — FlowServices (flow.xml), decision tables, service signatures (node.ndf), JDBC adapters, and SOAP connectors in a webMethods Integration Server codebase, or the equivalent artifacts in another legacy stack — and produce a characterization artifact for migration. Generic and reusable across legacy-to-target migrations. Use when analyzing what a legacy operation does before migrating it.
license: Proprietary
metadata:
  author: Neeraj
  version: "2.0"
---

# Legacy Source Analysis

Reusable techniques for reading a legacy codebase so a migration faithfully captures its behavior.
This skill is the generic "how". Concrete facts — the legacy source root, the project's package
names, the contract to cross-check against, where to write the artifact — are supplied by the
calling agent; do not assume specific paths here.

The detailed technique below is written against webMethods Integration Server, the layered
FlowService/decision-table/adapter shape this package was first built for. The same
principles — trace the full call graph, follow field lineage through every rename, extract rule
rows as golden fixtures, capture the exact downstream contract, classify every error code — apply
to other legacy stacks; substitute the equivalent source artifacts for `flow.xml`, `node.ndf`, and
`.decisiontable` files.

---

## The layered flow (typical shape)

A webMethods app usually layers each operation as:

```
API entry      a FlowService (flow.xml) per operation        — INVOKE chains + MAP nodes; the skeleton
   ↓
Orchestration  service FlowServices                          — sequences rule calls + data calls; MOST logic
   ↓
Rules          a business-rules service → decision tables    — business rule rows
Data adapters  JDBC adapter services                         — SQL operations
Connectors     SOAP/REST connector services                 — calls to peer systems
```

Read **all layers** — the API-entry flow alone is never enough; most logic lives in orchestration
and below. (The project's concrete package names for each layer are in its conventions file.)

## Reading `flow.xml`

A FlowService is visual logic serialized to XML. Key node types:

| Node | Meaning | Migration relevance |
|------|---------|---------------------|
| `<INVOKE SERVICE="...">` | Calls another service | The call sequence — order matters |
| `<MAP>` / `MAPTARGET` / `MAPSOURCE` | Renames/reshapes pipeline fields | **Silent field renames = business logic.** Capture every one. |
| `<BRANCH>` | Conditional (switch on a field) | Trace BOTH paths — tenant/variant-specific branches hide here |
| `<SEQUENCE EXIT-ON="FAILURE">` | Try block | Maps to try/catch |
| `<SEQUENCE EXIT-ON="DONE">` | Catch / cleanup | Error handling + the exact error codes/messages |
| `<LOOP>` | Iterate over a list | Maps to a Java loop/stream |

**Technique for large flow.xml** (they can be hundreds of KB): extract the call spine first, then
read MAP nodes and branches.
```bash
grep -o 'SERVICE="[^"]*"' flow.xml                       # the INVOKE spine
grep -n '<BRANCH\|<MAP\|MAPTARGET\|<LOOP' flow.xml        # control flow + field transforms
```
Ignore infrastructure INVOKEs (request-header fetch, logging start/end, JSON serialization,
get-last-error) — the target framework handles those. Focus on business INVOKEs and the MAP nodes
between them.

## Reading `node.ndf`

The service signature: `sig_in` (inputs) and `sig_out` (outputs, often a `rec_ref` to a canonical
doc type). Use it to confirm the operation's parameters and response shape — cross-check against the
project's API contract.

For every migrated operation, capture the signature explicitly. Include the `node.ndf` path, each
`sig_in` and `sig_out` field, webMethods type, list/document nesting, `rec_ref` target, and any
required/optional/null/empty semantics you can infer from the signature, validation flow, contract,
or downstream consumers. If optionality or null handling cannot be proven, record an open question
instead of guessing.

## Reading decision tables

Decision-table rows are the rule source for migration: each row is an input-condition ->
output-action pair. These rows are golden test data: conditions are inputs, actions are expected
outputs.

Follow `.claude/rules/migration-conventions.md` for the authoritative rule analysis source paths,
integration-reference scope, stale-source exclusions, fixture generator, and output locations.
Ignore repository rule-output directories during characterization inventory when the project
conventions classify them as migrated implementation assets instead of source evidence. Do not use a
stale/non-authoritative rule export to derive rule counts, fixtures, market coverage, or behavior
unless a human explicitly approves a named exception. If the authoritative decision-table artifact is
missing, block characterization instead of falling back to stale exports or the migrated rule implementation.

Per-tenant rule sets usually live in sibling folders; some tenants have extra tables others don't —
check every tenant's folder, don't trust one. Some systems also have shared or common rule
projects. Treat those as a separate shared corpus, not as another tenant/market column, and prove
from the wrapper namespace or project-name pipeline value whether a same-named table is coming from
the tenant project or the shared project.

### Rule corpus gate for domain migrations

When characterizing a decision-table-backed domain, complete the rule corpus gate before filling the report
template or handing off to design:

1. Inventory every market/tenant rule project and every shared/common rule project relevant to the
   domain. Count legacy source `.decisiontable` assets, migrated rule implementation assets, and
   committed fixtures.
2. Trace the domain FlowService/business-rule call path to the directly invoked decision tables.
3. Inspect outputs from directly invoked tables for shared/transitive dependencies, such as event
   names, rule names, partner interface keys, benefit/cashback identifiers, config keys, or error
   mappings that require another decision table to interpret behavior.
4. Classify every decision table in the checked market/tenant projects and shared/common projects
   as `domain-required`, `shared-required`, `used-by-other-domain`, `not-used-by-this-domain`,
   `unknown`, or `excluded-with-approved-reason`.
5. Generate candidate rule parity fixture data from the authoritative `.decisiontable` files for
   every `domain-required`, `shared-required`, and `unknown` table across every applicable market.
   Use the project-approved decision-table parser declared in migration conventions when one is
   available. Do not use a parser or export source that project conventions mark stale or
   disallowed.
6. Generate and include a rule-count matrix with one row per required/shared/unknown market/tenant
   decision table and one column per market/tenant, plus totals. Include a separate shared/common
   rule-count view when shared/common projects are present. Counts must come from source
   `.decisiontable` rule rows.
7. Block analyze approval while any `domain-required`, `shared-required`, or `unknown` table
   lacks fixtures, migrated assets, conversion-fidelity evidence, or an explicit human resolution.
8. If a migrated rule implementation already exists under repository `rules/`, verify it as a
   candidate implementation output rather than trusting it: compile/load or build path,
   module/package routing, model compatibility, source `.decisiontable` reconciliation, fixture/test
   reconciliation, and market isolation.

The characterization artifact must show this gate's evidence in the template's rule-corpus
sections. Do not rely on the template alone to discover missing tables after the analysis is done.

When project conventions define a decision-table fixture generator, use it to generate candidate
fixtures and a rule-count matrix from authoritative `.decisiontable` artifacts. Generated output must
be written to the fixture path pattern declared by project conventions. Prefer one fixture file per
decision-table/market pair, with the market/tenant tag still retained inside every row, so reviewers
can approve one table/market at a time. Generated rows remain candidate evidence until
SME/source-owner validation records any corrections. Only validated rows satisfy the golden-fixture
parity gate. Do not use a disallowed parser or stale export source as the rule-source path unless a
human explicitly approves a named exception.

Before analyze approval for a decision-table-backed domain, verify and document:
- the complete rule-project inventory for every market/tenant relevant to the domain, even when the
  domain directly uses only a subset of the market rule project;
- every decision table directly used by the domain, transitively required by a used/shared rule, or
  needed to evaluate/interpret that domain's rule outputs has committed fixture files under the
  project-declared rules fixture path pattern;
- every market/tenant relevant to the domain has its own required fixture file for each
  required/shared/unknown decision table;
- generated candidate fixture files exist for every required/shared/unknown decision table and were
  produced from `.decisiontable`, not `.jessML`;
- a decision-table rule-count matrix exists in the report showing source row counts per required
  table per market and totals;
- every legacy decision table in the checked market projects is classified as
  `domain-required`, `shared-required`, `used-by-other-domain`, `not-used-by-this-domain`,
  `unknown`, or `excluded-with-approved-reason`;
- `domain-required`, `shared-required`, and `unknown` tables are treated as blockers until fixtures,
  migrated assets, and design handling are available or the human reviewer explicitly resolves the
  classification;
- rule counts reconcile to legacy `.decisiontable` source for every required table, or
  exclusions are listed with source path, reason, impact, owner, and human approval status;
- parser/import defects or manual corrections are documented in the characterization report;
- the decision-table-to-target conversion fidelity audit is complete for every migrated or generated
  rule implementation that the design may use;
- every existing `rules/` implementation/model/test asset that the design may use has an
  implementation-shape verdict: `verified`, `verified-with-approved-gaps`, or `blocker`.

Do not treat "the current domain invokes seven rule services" as proof that only seven decision
tables matter. First inventory all tables in the market rule projects, then map the domain's
FlowService/business-rule call path to the directly required tables, and then inspect those outputs
for shared/transitive rule dependencies. A table can be outside the current domain only after it has
an explicit classification and evidence-backed reason. Unknown classification blocks design.

The conversion fidelity audit is mandatory because a converter can generate a syntactically valid
rule implementation while losing rule behavior. For each table/market, compare legacy
`.decisiontable` source, generated fixtures, the migrated rule implementation, and generated tests.
Record:
- source decision-table file, rule implementation file, fixture file, and test file;
- source row count, fixture row count, migrated rule count, generated test count, and exclusions;
- compile/load or build result, module/package routing, model class compatibility, and
  market-isolation result for existing `rules/` assets;
- helper functions and operators used by source rows, including list/range/date helpers and
  invocation-time guards, with the exact translation or a blocker;
- every condition discriminator and action field that must survive conversion;
- duplicate normalized condition sets with conflicting outputs;
- broad subset rules that can overwrite more-specific outputs;
- row activation semantics such as sequential/first-match/order dependence, if present;
- verdict: `pass`, `pass-with-documented-exclusions`, or `blocker`.

Treat contradictory same-input fixtures, collapsed source conditions, unsupported helper functions,
and unexplained overwrite behavior as analyze blockers. Do not defer them to coding.

Do not stop at "fixture missing" when the authoritative `.decisiontable` source is available.
Generate candidate fixtures into the project-declared per-table/per-market fixture path and the
count matrix first, then mark SME validation/correction status as pending or blocked if review is
still required.

## Reading adapters & connectors

- Each JDBC adapter service = one SQL operation (SELECT/INSERT/UPDATE/DELETE). Map it to the
  equivalent endpoint on the target data layer.
- Each SOAP/REST connector = one call to a peer system. In the new system this typically becomes a
  call through the target data/integration layer, not a direct call.
- Inspect the adapter or connector `node.ndf`, not just the calling FlowService. Capture declared
  inputs, outputs, adapter type, connection/config references, SQL/stored-procedure or connector
  operation metadata when present, and any retry/timeout settings. If these details are not encoded
  in source, record the checked path and mark the claim as not found or an open question.
- For SOAP/REST dependencies, capture the exact wire contract instead of just the dependency name:
  protocol, runtime endpoint or config-key source, endpoint path shape, HTTP method when REST,
  SOAP namespace, root localPart, SOAP action when used, schema version shape and value, request
  fields, response fields, fault shape, propagated headers/auth, and timeout/retry behavior when
  discoverable.
- Distinguish environment-specific URL configuration from code-level protocol/schema constants. A
  URL normally belongs in runtime config; SOAP namespace, localPart, schemaVersion, REST method, and
  path template must come from WSDL/XSD/source annotations or connector metadata, not from guessed
  examples.
- When a downstream service source tree is available through project conventions, inspect its
  contract evidence before concluding protocol or schema shape. For Spring Boot targets, look for
  `@RestController`, `@RequestMapping`, `@PayloadRoot`, Spring-WS servlet mappings,
  `DefaultWsdl11Definition`, WSDL/XSD resources, and generated schema classes. Record checked paths
  and mark missing evidence as `not-found` or `open-question`.
- Capture dependency behavior, not just dependency names: protocol, source service path, target
  replacement, configuration key or endpoint source, auth/header propagation, timeout/retry behavior
  where discoverable, and the exact fault/error mapping.
- For writes and other side effects, identify operation order, transaction boundary, rollback or
  compensation behavior, idempotency or duplicate guards, and partial-failure outcomes.

## Reading functional config and reference data

Legacy webMethods flows often read configuration through shared config services, package-specific
wrappers, cache lookups, flat files, deployment-mounted files, database-backed config tables, or
environment-specific property files. Treat these as migration evidence when the returned value
affects functional behavior, not merely infrastructure.

When a traced call graph invokes a config/reference lookup:

- Capture the config service or wrapper path, `node.ndf` signature when present, and exact input
  fields used to construct the lookup key.
- Trace the returned value through pipeline lineage: branch conditions, downstream endpoint
  selection, rule inputs, partner/interface/event keys, response fields, error mappings, defaults,
  and fallback behavior.
- Identify the value source from project conventions: source file, deployment-mounted file,
  database/config table, environment variable, secret store, or checked-but-missing source.
- Record environment, tenant, market, or service-family variance when the source exposes it.
- Distinguish functional config/reference data from secrets. List key names, value shape, behavior
  impact, and source path, but do not copy credentials, tokens, private keys, full payload samples,
  or personal/health data into artifacts.
- If the source file is a placeholder, generated at deployment, or absent, check the project
  conventions for an approved runtime/deployment config evidence path. If no approved path exists,
  raise an open question instead of assuming the default.
- Classify the migration action needed: target environment property, application config,
  secret-backed property, DAL/reference-data endpoint, test fixture, static constant approved by
  design, or unresolved design gap.

Do not treat config as "non-functional" by default. A URL, feature switch, market mapping,
business threshold, error translation key, or partner list stored in config is part of observable
legacy behavior and must be handed to design.

## Reading error handling

Error behavior is part of the public contract even when it is implemented through shared utilities,
translation tables, or propagated dependency faults. Do not report only the codes that are directly
hardcoded in the API-entry FlowService.

For every characterized domain, build a complete error-code inventory and classify each code:

- `domain-direct` — set or thrown directly by the domain entry flow, domain utility, orchestration
  service, branch/catch path, or domain wrapper.
- `dependency-propagated` — copied from a downstream DAL/SOAP/REST response, wrapper
  `/Exception/reasonCode`, `ServiceFault/Code`, SOAP fault code, or equivalent dynamic error field.
- `shared-translation` — present in an invoked shared/common error translation, interface, or
  logging decision table used by the domain's error path, even when the domain flow does not
  directly set that code.
- `domain-service-unused` — found in the domain's source package or invoked service family but not
  reachable from the traced operation call graph; include the checked path and exclusion reason.
- `shared-unused` — present in a shared/common error corpus that the domain can invoke, but not
  proven reachable from this domain; include it when the shared corpus is part of the domain's
  error handling evidence.
- `unknown-reachability` — discovered in a relevant source or fixture, but reachability cannot be
  proven or disproven from available source.

The characterization report must mention every error code discovered in these categories. It may
summarize the high-risk/user-visible codes in the main error table, but it must also include or link
to a complete inventory table/appendix that names every code, source, translation output, usage
classification, and evidence confidence. A generated fixture row for an error translation table is
evidence that the code exists in the shared error corpus; it is not evidence that a domain directly
throws the code unless the flow/call graph proves reachability. Preserve that distinction in the
report instead of omitting the code.

## Existing / partial target implementation scan

Some migrations start after a Spring Boot module, rule asset set, tests, or DTOs already exist.
That code can reduce implementation work, but it is not legacy truth. Treat it as target
implementation baseline and gap evidence only.

Infer the candidate target implementation from project conventions and repository structure. Use
the configured target module pattern when present, then check domain-name variants such as
singular/plural forms, contract tags/package names, and sibling domain modules. If no module exists,
record the checked paths as `not-found`. If multiple plausible modules or assets exist, ask the
human which one is in scope before marking characterization approval-ready.

When a candidate target implementation exists, inspect it during characterization after the legacy
behavior is understood:

- inventory existing controllers, services, DAL clients, DTOs, rule facades/assets, config, and
  tests for the domain;
- map each existing class or asset to the characterized operation, rule table, dependency, or test
  obligation it appears to cover;
- classify each item as `reuse`, `refactor`, `replace`, `defer`, or `unknown`, with a reason;
- record mismatches between existing comments/code and proven legacy behavior, such as reduced
  market scope, hardcoded data, skipped branch paths, missing rule parity, contract differences,
  alternate DAL endpoints, or partial tests;
- keep the existing implementation evidence separate from `Migration Sources Checked` so reviewers
  do not confuse target code with authoritative legacy source.

If existing implementation exists and is not scanned, the characterization is incomplete. If it
exists but cannot be reconciled to legacy behavior, raise a numbered open question or blocker for
design instead of silently accepting or discarding it.

## Asking questions during analysis

Do not guess through uncertainty that changes scope, source priority, market coverage, public
behavior, side effects, rule classification, or whether existing target code should be trusted.

Ask the human or source owner during analysis when:

- two authoritative-looking sources conflict and project conventions do not define a winner;
- a behavior cannot be interpreted without business meaning, such as whether a legacy branch is
  still supported;
- a source gap prevents classifying a decision table, connector, operation, market, or side effect;
- existing target implementation contradicts proven legacy behavior and the correct migration
  direction is not a technical choice;
- proceeding would require excluding a market, rule table, branch, write path, or public error.

If the question does not block continued evidence gathering, continue analysis and record it under
`Open Questions / Decisions Required` with impact, options, recommendation, owner, and required
phase before resolution. If the question blocks interpretation of evidence, stop and ask before
marking characterization ready for approval.

## What to produce (the characterization / migration report)

Use the canonical report template at
`templates/characterization-report.md` when producing the characterization artifact. Keep the
template with this skill because the report shape is part of the WebMethods-analysis capability, not
a project-specific implementation detail. Project-specific facts still come from the calling agent's
conventions file.

The template headings are the standard output contract. Do not replace them with ad-hoc headings.
If a section does not apply, keep the section and say why. If a mandatory section cannot be
completed from source, keep the section, list paths checked, and raise a numbered open question with
impact, options, recommendation, and owner.

Structure the report for multiple review personas without losing evidence:
- **Business SME / product owner** needs scope, functional behavior, market differences, business
  decisions, user-visible errors, and open approval asks.
- **webMethods SME** needs FlowService structure, MAP/pipeline lineage, `node.ndf`, adapter,
  connector, and rule-source evidence.
- **Tester / QA** needs fixtures, edge cases, branch outcomes, rule parity coverage, API parity
  scenarios, and failure modes.
- **Developer** needs contract inputs, DTO/rule/DAL mappings, dependency behavior, target handoff
  risks, and implementation blockers.
- **Architect / NFR reviewer** needs transaction boundaries, idempotency, timeouts, retries,
  auth/header propagation, observability, data consistency, and operational risks.

Write the artifact as a progressive review document:
1. Persona review guide and executive review first, so each reviewer knows where to focus.
2. Functional behavior and non-functional behavior summaries next, written in business/testable
   terms and tied back to evidence confidence.
3. Rule behavior and coverage next, because rules often define the observable domain behavior.
4. Technical legacy analysis next, preserving the detailed webMethods evidence.
5. Design/code handoff, open questions, and evidence appendix last.

Use evidence-confidence markers on characterization claims:
- `proven` — directly supported by cited source paths and line/element references where practical;
- `inferred` — reasoned from multiple sources; explain the inference;
- `not-found` — expected evidence was searched for and absent; list checked paths;
- `open-question` — unresolved behavior requiring human or source-owner decision.

In **Migration Sources Checked**, list only migration evidence: contracts, legacy source files,
rule assets, adapters/connectors, fixtures, generated evidence, and checked-but-missing migration
sources. Do **not** list agent instructions, LLM behavior rules, process files, or developer tooling
as migration sources.

The required detail set is:
1. **Persona review guide** — who should review which sections and what approval/risk questions
   each persona owns.
2. **Executive review** — migration scope, markets, behavior summary, confidence, blockers, and
   explicit human decisions.
3. **Functional behavior** — operation behavior, business decisions, market differences, rule
   outcomes, user-visible errors, side effects, and testable examples.
4. **Non-functional behavior** — transaction, idempotency, retry/timeout, auth/header, observability,
   failure, and data-consistency behavior.
5. **Architecture & context** — code structure, structural fit, dependencies, migration scope, and
   sequencing.
6. **Domain boundary discovery** — start from the contract operation and the project-convention
   entry source, then trace every business INVOKE across orchestration, rules, data adapters,
   connectors, shared utilities, and integration/proxy packages before deciding scope. List included
   packages/services/docs/rules/data dependencies, explicit exclusions, paths checked, and evidence
   confidence.
7. **Operation inventory** — each operation, its flow.xml path, its contract path.
8. **Service signature & pipeline schema** — `node.ndf` path; `sig_in`/`sig_out` fields, types,
   required/optional/null/empty semantics, `rec_ref` doc types, nested documents/lists, and fields
   present in the pipeline but absent from the public contract.
9. **Per-operation call sequence** — the ordered business INVOKEs across the layers.
10. **Pipeline variable lineage** — variables set, overwritten, dropped, or renamed; first producer,
   MAP aliases, later consumers, branch-specific values, and the output or side effect they
   influence.
11. **Field-mapping table** — every MAP-node rename (legacy field → response field).
12. **Branch logic** — each conditional, both paths, any tenant/variant specificity.
13. **Dependency behavior register** — each DAL adapter, SOAP/REST connector, config/reference
   lookup, rule table, or peer service with protocol, source path, target replacement, config key,
   auth/header propagation, timeout/retry behavior if discoverable, failure mapping, readiness, and
   exact downstream contract evidence for any SOAP/REST peer dependency.
14. **Adapter and connector `node.ndf` inventory** — for every adapter or connector dependency,
   capture the `node.ndf` path, adapter/connector type, `sig_in`, `sig_out`, config or connection
   references, SQL/stored-procedure or connector operation metadata if present, checked-but-missing
   metadata, and evidence confidence.
15. **Functional config and reference data** — every config/reference lookup that affects behavior,
   including key construction, source file/table/env evidence, env/tenant/market/service variance,
   value consumers, defaults/fallbacks, secret-safety handling, target replacement options, and
   design action needed.
16. **Side effects & transaction boundaries** — writes performed, order, transaction endpoint or
   boundary, rollback/compensation behavior, idempotency or duplicate guard, partial-failure
   outcome, and parity fixture needed.
17. **Data operations** — which tables/SQL ops, mapped to target data-layer endpoints; **flag
   multi-step transactional ops and any stateful-pipeline ordering** (a field set in one step and
   read in a later one).
18. **Rule corpus inventory and domain rule coverage** — all legacy market decision-table projects
    checked, every source decision table classified for the domain, directly required and
    shared/transitive required tables, missing/extra migrated assets, and explicit exclusions.
19. **Error codes/messages** — complete error-code inventory with exact strings/status mappings
   from domain branches, catch paths, dependency faults, dynamic propagated error fields, and
   invoked shared/common translation tables; classify each code as direct, propagated,
   shared-translation, unused, or unknown reachability.
20. **Golden fixtures** — input→output pairs (from legacy `.decisiontable` rows + contract examples) for parity
   tests, including negative/edge cases for missing required fields, blank-vs-absent values, empty
   results, dependency failures, and partial-write cases where applicable.
21. **Rule parity fixture coverage** — for decision-table-backed domains, the legacy source
   `.decisiontable` artifacts reviewed, generated fixture paths under the project-declared
   per-table/per-market fixture layout, required decision tables, in-scope markets,
   source-vs-fixture rule counts, SME validation status, corrections, and any blocking fixture gaps.
22. **Decision-table-to-target conversion fidelity audit** — for every migrated or generated rule
   implementation used by the domain, the source-vs-implementation/test reconciliation, unsupported
   helper/operator inventory, duplicate condition conflicts, broad-overwrite risks, row activation
   semantics, and verdict.

Each detail section is mandatory. If a section does not apply, say why. If a section cannot be
completed from available source, add a numbered open question with the paths checked and the
migration risk.

## Pitfalls

- **Don't skim flow.xml.** Branches deep in an INVOKE chain may fire only for specific tenants.
- **Don't ignore MAP nodes.** A missed rename means the wrong field name in the response.
- **Don't ignore node.ndf.** A missed `sig_in`/`sig_out` field or `rec_ref` can hide optionality,
  nested document structure, or fields that only appear downstream.
- **Don't lose pipeline lineage.** A field set early and consumed later is business logic even when
  no final response rename is visible.
- **Don't reduce dependencies to names.** Timeout, retry, auth/header propagation, and fault mapping
  can be observable behavior.
- **Don't infer SOAP/REST contracts from examples.** For peer-service calls, prove namespace,
  localPart, schemaVersion, method/path, request/response fields, and fault shape from WSDL/XSD,
  connector metadata, or available downstream source. A reachable URL with the wrong payload
  contract is still a migration bug.
- **Don't miss functional config.** Config lookups, mounted config files, cached reference data,
  and environment-specific values can control branches, endpoints, market mappings, thresholds,
  and error behavior. Trace them like any other dependency and hand them to design.
- **Don't skip adapter or connector node.ndf files.** The calling flow shows that a dependency is
  invoked; the adapter/connector metadata may be the only place that exposes signature, connection,
  SQL/stored-procedure, and runtime settings.
- **Don't flatten side effects.** Write ordering, transaction boundaries, rollback, and duplicate
  guards are part of the legacy behavior.
- **Don't trust one tenant.** Check every tenant's rule folder for variants.
- **Don't confuse domain-used tables with the full checked rule corpus.** A domain migration stays
  domain-scoped, but characterization must still inventory every rule table in every relevant market
  and explicitly classify tables that are not required by the domain.
- **Don't ignore shared/transitive rule dependencies.** If a domain-required table emits event
  names, rule names, partner interfaces, benefit/cashback identifiers, or config keys that require
  another rule table to interpret or evaluate the domain behavior, include that table as
  `shared-required` for this domain.
- **Don't trust a generated rule implementation without a conversion audit.** A row can compile and
  still be wrong if helper functions, list/range/date guards, or row ordering were dropped.
- **Don't use stale rule exports as source evidence.** When project conventions identify
  decision-table artifacts as the rule source of truth, missing source decision tables block
  characterization.
- **Don't report only directly thrown error codes.** If an invoked shared/common error translation
  table contains additional codes, or a dependency can propagate dynamic reason codes, classify and
  report them as shared/propagated/unused/unknown instead of omitting them.
- **Don't migrate legacy bugs as features.** When legacy ≠ contract, the contract wins.
