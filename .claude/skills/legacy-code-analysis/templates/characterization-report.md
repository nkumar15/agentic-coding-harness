# <Domain Name> Characterization

Status: analyze phase artifact for human review. This document characterizes the legacy
webMethods implementation only. It does not propose or implement the target design.

## Evidence Confidence Legend

Use these markers in every evidence-bearing table or claim. Do not leave confidence implicit.

| Marker | Meaning | Required handling |
| --- | --- | --- |
| `proven` | Directly supported by cited source paths and, where practical, flow step, XML element, rule row, or line reference. | Use for behavior that can be implemented or designed from source. |
| `inferred` | Reasoned from multiple sources, but not directly stated in one source. | Explain the inference and list the supporting sources. |
| `not-found` | Expected evidence was searched for and absent. | List checked paths and the risk. |
| `open-question` | Behavior cannot be proven and needs human or source-owner decision. | Add a numbered item under Open Questions / Decisions Required. |

## Persona Review Guide

Use this table to route review. Each persona should review its listed sections and raise approval
questions in Open Questions / Decisions Required.

| Persona | Primary sections | Must validate | Approval / risk focus |
| --- | --- | --- | --- |
| Business SME / product owner | Executive Review; Functional Behavior Review; Error Codes And Messages; Open Questions / Decisions Required | Business outcomes, market differences, user-visible errors, in/out of scope behavior | Whether the characterized behavior matches intended business behavior |
| webMethods SME | Technical Legacy Analysis sections; Service Signature And Pipeline Schema; Pipeline Variable Lineage; MAP-Node Field Renames; Adapter And Connector `node.ndf` Inventory; Rule Corpus Inventory And Domain Coverage | FlowService call path, pipeline state, signatures, adapter/connector metadata, rule-source interpretation | Whether source evidence was read correctly and no legacy behavior was missed |
| Tester / QA | Functional Behavior Review; Rule Behavior Review; Golden Fixtures; Decision-Table-To-Target Conversion Fidelity Audit; Error Codes And Messages | Test scenarios, edge cases, fixture coverage, rule parity risks, negative/failure cases | Whether enough evidence exists to build parity tests |
| Developer | Architecture And Context; Operation Inventory; Dependency Behavior Register; Data Operations; Design And Code Handoff | DTO/rule/DAL mappings, dependencies, sequencing, implementation blockers | Whether design/coding can proceed without guessing |
| Architect / NFR reviewer | Non-Functional Behavior Review; Dependency Behavior Register; Side Effects And Atomic Write Boundaries; Data Operations; Design And Code Handoff | atomic writes, retries, timeouts, idempotency, auth/header propagation, data consistency | Whether operational and integration risks are understood |

## Executive Review

Write this section in business-readable terms. Keep it short but decision-ready.

- Domain / capability:
- Markets in scope:
- Operations in scope:
- Operations explicitly out of scope:
- Business behavior summary:
- Market-specific behavior summary:
- Rule behavior summary:
- Side effects or writes:
- Major confidence gaps:
- Approval blockers:
- Recommended human decisions:

### Review Verdict

| Area | Status | Evidence confidence | Notes / decision needed |
| --- | --- | --- | --- |
| Functional behavior | `<ready/partial/blocker>` | `<proven/inferred/not-found/open-question>` | `<notes>` |
| Rule behavior | `<ready/partial/blocker>` | `<proven/inferred/not-found/open-question>` | `<notes>` |
| Integration behavior | `<ready/partial/blocker>` | `<proven/inferred/not-found/open-question>` | `<notes>` |
| Non-functional behavior | `<ready/partial/blocker>` | `<proven/inferred/not-found/open-question>` | `<notes>` |
| Design handoff readiness | `<ready/partial/blocker>` | `<proven/inferred/not-found/open-question>` | `<notes>` |

### Characterize Phase Checklist

Use this checklist as the human-readable completion view. A checked item means the report includes
source evidence or an explicit blocker/open question; it does not mean the behavior is automatically
approved.

- [ ] Operations in scope are listed and cross-checked against the contract.
- [ ] Domain boundary discovery starts from the contract operation and traces the invoked call graph;
      included and excluded packages are recorded with evidence.
- [ ] API-entry FlowServices, orchestration FlowServices, rules, adapters, and connectors are traced.
- [ ] Relevant API service, utility service, adapter/connector, and doc-type `node.ndf` files are
      inspected or listed as not found.
- [ ] Pipeline variable lineage records first producer, MAP aliases, overwrites/drops,
      branch-specific values, consumers, and observable outputs or side effects.
- [ ] MAP-node field renames are captured as migration behavior, not treated as formatting.
- [ ] Branch, loop, error/catch, and dependency-failure paths are represented as testable behavior.
- [ ] Dependency behavior covers target replacement, config/auth/header propagation, timeout/retry
      evidence, and failure mapping.
- [ ] Functional config/reference-data lookups are traced from lookup key construction through
      value source, consumers, env/market/service variance, fallback/default behavior, and target
      migration action.
- [ ] Side effects, writes, atomic write boundary, rollback/compensation, idempotency, and
      partial-failure outcomes are explicit or marked not found/open question.
- [ ] Rule corpus inventory covers every applicable market rule project, plus shared/common rule
      projects when present, and classifies every decision table.
- [ ] Candidate rule parity fixtures are generated from authoritative `.decisiontable` files for
      every `domain-required`, `shared-required`, and `unknown` table across applicable markets and
      shared/common rule projects.
- [ ] A per-market decision-table rule-count matrix is included for required/shared/unknown market
      tables, and a separate shared/common rule-count view is included when shared/common rule
      projects are present.
- [ ] `domain-required`, `shared-required`, and `unknown` decision tables have fixtures, migrated
      assets, conversion evidence, or an explicit blocker/human decision.
- [ ] Golden rule/API fixtures and edge/failure scenarios are identified for tester review.
- [ ] Decision-table-to-target conversion fidelity is audited for every rule asset the design may wire.
- [ ] Error-code inventory includes direct domain codes, dependency-propagated dynamic codes,
      invoked shared/common translation-table codes, relevant but unused codes, and unknown
      reachability codes; each code has source, mapping, usage classification, and evidence
      confidence.
- [ ] Existing or partial target implementation has been inventoried and gap-reviewed, or the report
      states that no current implementation was found.
- [ ] Open questions include impact, options, recommendation, owner, and required phase before
      resolution.
- [ ] Design handoff identifies what design must decide and what code/tests must later implement.

## Migration Sources Checked

List only migration evidence. Do not list agent instructions, LLM behavior rules, process files, or
developer tooling as sources.

- REST/API contract:
  - `<path>`
- Target data-layer contract or mapping:
  - `<path>`
- Legacy API-entry FlowServices:
  - `<flow.xml path>`
  - `<node.ndf path>`
- Legacy orchestration FlowServices:
  - `<flow.xml path>`
  - `<node.ndf path>`
- Legacy utility services:
  - `<flow.xml path>`
  - `<node.ndf path>`
- Shared services and peer connectors:
  - `<service or connector path>`
- Adapter and connector metadata:
  - `<adapter/connector node.ndf path>`
- Functional config/reference-data sources:
  - `<config lookup flow/node.ndf path>`
  - `<source config file/table/env/deployment-mounted file path, with secret values omitted>`
- Legacy rule assets:
  - `<source decision-table path from migration conventions>/<table>.decisiontable>`
- Migrated rule assets:
  - `<migrated rule asset path from migration conventions>` only as migrated implementation evidence, not source evidence
- Existing fixtures:
  - `<fixture path>`
- Generated evidence reviewed, if any:
  - `<path and validation status>`

Checked but not found:

- `<expected path or source>`

## Existing / Partial Target Implementation Baseline

Use this section when a Spring Boot module, rule assets, DTOs, tests, or other target implementation
already exists for the domain. Existing target code is not authoritative legacy evidence. It is
baseline/gap evidence for design.

If no existing target implementation is found, state the paths checked and mark the section
`not-found`. If the candidate target module or assets are ambiguous, list the candidates and create
a numbered open question before characterization approval.

Discovery method:

- Target module pattern checked:
- Domain aliases checked:
- Contract tags/package names checked:
- Candidate modules/assets found:
- Human clarification needed: `<yes/no; question id if yes>`

| Existing target file / asset | Current role | Characterized behavior it appears to cover | Gap or mismatch vs legacy characterization | Design handling | Evidence confidence |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<controller/service/DAL/DTO/rule/test/config>` | `<operation/rule/dependency/test obligation>` | `<none or mismatch>` | `<reuse/refactor/replace/defer/unknown>` | `<proven/inferred/not-found/open-question>` |

Existing implementation design implications:

- `<what the architecture must account for before coding>`

Existing implementation blockers / open questions:

- `<question id or none>`

## Functional Behavior Review

Summarize observable behavior in a form business SMEs and testers can review before reading the
technical evidence.

### Functional Decision Summary

| Operation | Business decision / outcome | Inputs affecting decision | Outputs affected | Market differences | Rule/dependency source | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `<operation>` | `<decision/outcome>` | `<fields>` | `<response fields/side effects>` | `<market-specific behavior>` | `<rule/flow/adapter>` | `<proven/inferred/not-found/open-question>` |

### Functional Scenarios And Edge Cases

| Scenario | Inputs / preconditions | Expected legacy behavior | Source evidence | Fixture / test need | Evidence confidence |
| --- | --- | --- | --- | --- | --- |
| `<happy/negative/edge/failure case>` | `<inputs>` | `<expected outcome>` | `<path/rule row/flow branch>` | `<fixture path or gap>` | `<proven/inferred/not-found/open-question>` |

### Market Behavior Matrix

| Market | Behavior variant | Required rule tables / dependencies | Known gaps | Evidence confidence |
| --- | --- | --- | --- | --- |
| `<market>` | `<same/different behavior>` | `<tables/dependencies>` | `<gap or none>` | `<proven/inferred/not-found/open-question>` |

## Rule Behavior Review

Summarize rule behavior for SMEs and testers. Detailed rule inventories remain in Rule Corpus
Inventory And Domain Coverage, Golden Fixtures, and Decision-Table-To-Target Conversion Fidelity Audit.

| Rule area | Business meaning | In-scope markets | Required tables | Fixture status | Conversion fidelity status | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `<pricing/config/rates/etc.>` | `<business purpose>` | `<markets>` | `<tables>` | `<covered/partial/blocker>` | `<pass/partial/blocker/not available>` | `<proven/inferred/not-found/open-question>` |

## Non-Functional Behavior Review

Summarize behavior that affects operations, reliability, security pass-through, and data
consistency. If source does not expose a setting, record `not-found` with checked paths.

| Concern | Legacy behavior | Source evidence | Migration risk | Test / design implication | Evidence confidence |
| --- | --- | --- | --- | --- | --- |
| Auth/header propagation | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Timeout / retry | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Atomic write boundary | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Idempotency / duplicate guard | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Partial failure handling | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Observability / audit logging | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |
| Data consistency / ordering | `<behavior>` | `<path>` | `<risk>` | `<design/test implication>` | `<proven/inferred/not-found/open-question>` |

## Technical Legacy Analysis

The sections below preserve the detailed source evidence needed by webMethods SMEs, developers,
architects, and testers. Do not remove these sections when the executive/functional summaries are
short.

## Architecture And Context

### Domain Boundary Discovery

Use the project migration conventions for concrete contract paths, legacy source roots, package
roles, source priorities, and excluded sources. Do not infer scope from a single folder name.

| Operation | Contract path / method | Entry FlowService + `node.ndf` | Invoked call graph followed | Included domain scope | Explicit exclusions | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `<operation>` | `<method path>` | `<flow.xml and node.ndf>` | `<business INVOKEs across rules/data/connectors/utilities>` | `<packages/services/docs/rules/data deps included>` | `<sibling packages/source snapshots/rule assets excluded with reason>` | `<proven/inferred/not-found/open-question>` |

Discovery notes:

- Contract operation used as the starting point:
- Project-convention entry package/source root used:
- Business INVOKEs followed beyond the entry flow:
- Shared/common utilities or integration/proxy packages included, with reason:
- Sibling packages or legacy source snapshots excluded, with checked paths:
- Remaining boundary questions:

### Code Structure

Explain how the legacy code for this domain is organized.

| Layer | Package / namespace | Element | Source |
| --- | --- | --- | --- |
| API entry | `<namespace>` | `<operation>` | `<flow.xml/node.ndf>` |
| Orchestration | `<namespace>` | `<service>` | `<flow.xml/node.ndf>` |
| Rules | `<namespace>` | `<decision table>` | `<decision table / rule implementation>` |
| Data adapter | `<namespace>` | `<adapter>` | `<adapter path>` |
| Connector | `<namespace>` | `<connector>` | `<connector path>` |

### Structural Fit

Describe where this domain sits in the system and include a small text diagram.

```text
<caller>
  -> <API entry>
  -> <orchestration>
  -> <rules/data/connectors>
  -> <response>
```

### Dependencies

| Direction | Dependency | Behavior | Status | Evidence confidence |
| --- | --- | --- | --- | --- |
| inbound/outbound | `<dependency>` | `<what it provides>` | `<available / missing / out of scope>` | `<proven/inferred/not-found/open-question>` |

### Migration Scope And Sequencing

- Operations:
- Decision tables:
  - Full checked rule corpus:
  - Domain-required tables:
  - Shared-required tables:
  - Tables explicitly excluded from this domain:
- Data operations:
- Connectors:
- Side effects:
- Sequencing implications:

## Operation Inventory

| Operation | Contract path | Legacy service | Characterization status | Evidence confidence |
| --- | --- | --- | --- | --- |
| `<operation>` | `<method path>` | `<service>` | `<status>` | `<proven/inferred/not-found/open-question>` |

### Contract Inputs

Headers:

- `<header>`

Query/path/body fields:

- `<field>`: `<required/optional, type, behavior>`

Contract vs legacy divergences:

- `<divergence and decision/open question>`

## Service Signature And Pipeline Schema From `node.ndf`

For each operation/service, capture signature exactly from `node.ndf`.

### `<service>`

- `node.ndf`: `<path>`
- Evidence confidence: `<proven/inferred/not-found/open-question>`
- `sig_in`:
  - `<field>`: `<type/dimension/rec_ref/nullability if known>`
- `sig_out`:
  - `<field>`: `<type/dimension/rec_ref/nullability if known>`
- Runtime metadata:
  - retry:
  - timeout:
  - circuit breaker:
  - validator settings:
- Fields present in pipeline but absent from public contract:
  - `<field and behavior>`

Unproven schema details:

- `<gap and open-question reference>`

## Pipeline Variable Lineage

Track values from first producer to final consumer.

| Pipeline variable | Source | Transform or lineage | Consumers | Evidence confidence |
| --- | --- | --- | --- | --- |
| `<variable>` | `<producer>` | `<MAP aliases, overwrites, drops, branch-specific values>` | `<response/rule/DAL/side effect>` | `<proven/inferred/not-found/open-question>` |

## MAP-Node Field Renames

In webMethods, a MAP node is the visual-flow step that copies, drops, sets, or reshapes values in
the runtime pipeline. For migration, a MAP-node field is any source or target field touched by those
MAP steps. These mappings are business behavior because they define how legacy internal names become
public API response names, DAL/query inputs, rule inputs, log fields, and exception fields.

| Legacy source field | Target field | Applies in | Notes | Evidence confidence |
| --- | --- | --- | --- | --- |
| `<source>` | `<target>` | `<operation/branch>` | `<rename/recase/type conversion>` | `<proven/inferred/not-found/open-question>` |

## Per-Operation Call Sequence

### `<operation>`

1. `<business call or branch>`
2. `<business call or branch>`

Infrastructure calls may be noted separately when they affect observable logging/error behavior.

## Branch Logic

| Location | Condition | True path | False/default path | Migration risk | Evidence confidence |
| --- | --- | --- | --- | --- | --- |
| `<flow/service>` | `<condition>` | `<behavior>` | `<behavior>` | `<risk>` | `<proven/inferred/not-found/open-question>` |

## Dependency Behavior Register

| Dependency | Used by | Behavior validated from source | Config/auth/header/timeout/retry/failure mapping | Evidence confidence |
| --- | --- | --- | --- | --- |
| `<dependency>` | `<operation/service>` | `<behavior>` | `<mapping or gap>` | `<proven/inferred/not-found/open-question>` |

## Downstream Contract Evidence

For every SOAP connector, REST connector, DAL wrapper, peer service, or integration/proxy
dependency that crosses a process boundary, record the exact callable contract. Keep runtime URL
configuration separate from protocol/schema constants. If downstream source is available, inspect
controller/endpoint annotations, servlet mappings, WSDL/XSD resources, generated schema classes, or
connector metadata before inferring protocol.

| Dependency | Used by | Protocol | Runtime endpoint / config source | Contract evidence checked | Operation / method | Namespace / localPart / path template | Schema version / action | Request mapping | Response mapping | Fault/error mapping | Test obligation | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<dependency>` | `<operation/service>` | `<SOAP/REST/other>` | `<env/config/service URL>` | `<WSDL/XSD/source annotation/node.ndf/path checked>` | `<SOAP op or HTTP method>` | `<namespace+localPart or REST path>` | `<schemaVersion/SOAPAction/n-a>` | `<legacy fields -> request>` | `<response -> pipeline/DTO>` | `<fault/status -> error>` | `<unit/API parity/contract test>` | `<proven/inferred/not-found/open-question>` |

## Functional Config And Reference Data

Use this section for config/reference lookups that affect functional behavior. Examples include
feature switches, market mappings, downstream URL selection, rule inputs, peer/interface/event
keys, thresholds, error translation keys, and fallback/default values. Do not copy secrets or
personal/health data into this artifact.

| Lookup / key | Used by | Key construction evidence | Value source evidence | Value consumers / behavior impact | Env / tenant / market / service variance | Default / fallback / missing behavior | Target migration action | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<service + key>` | `<operation/service>` | `<flow/node.ndf/MAP evidence>` | `<file/table/env/deployment-mounted file or not-found>` | `<branch/endpoint/rule/error/response effect>` | `<variance or none>` | `<fallback/gap>` | `<env property/secret/app config/DAL/static approved/gap>` | `<proven/inferred/not-found/open-question>` |

Config evidence gaps:

- Sources checked:
- Placeholder or generated-at-deploy files found:
- Secrets or sensitive values intentionally omitted:
- Human decisions needed:

## Adapter And Connector `node.ndf` Inventory

For every JDBC adapter, SOAP connector, REST connector, or shared peer-service dependency, inspect
its own `node.ndf` in addition to the FlowService that invokes it. This section is mandatory even
when the dependency is read-only or later mapped through the DAL.

| Dependency | node.ndf path | Type | sig_in | sig_out | Connection/config reference | Operation metadata | Checked but not found | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<adapter/connector/service>` | `<path>` | `<JDBC/SOAP/REST/shared-service>` | `<fields/types/rec_refs>` | `<fields/types/rec_refs>` | `<connection alias/env/config key>` | `<SQL/stored proc/connector op/method if encoded>` | `<missing metadata searched for>` | `<proven/inferred/not-found/open-question>` |

For JDBC adapters, record whether the adapter is `SELECT`, `INSERT`, `UPDATE`, `DELETE`, stored
procedure, or unknown. For SOAP/REST connectors, record the connector operation, endpoint/config
source, propagated headers/auth, and timeout/retry/fault settings when source exposes them. If the
`node.ndf` lacks these details, list the exact file checked and raise an open question if the gap
can change observable behavior.

## Side Effects And Atomic Write Boundaries

- Business writes:
- Logging/audit effects:
- External side effects:
- Atomic write boundary:
- Rollback/compensation:
- Idempotency or duplicate guard:
- Partial-failure outcome:
- Evidence confidence:

If a category does not apply, state why.

## Data Operations

| Data operation | Legacy source | Adapter node.ndf | Inputs | Output | Target mapping status | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `<operation>` | `<adapter/SQL/service>` | `<path>` | `<inputs>` | `<outputs>` | `<target endpoint or gap>` | `<proven/inferred/not-found/open-question>` |

Flag stateful-pipeline ordering where a value produced earlier is consumed by a later data operation.

## Rule Corpus Inventory And Domain Coverage

Domain migrations remain domain-scoped. Do not generate or wire every rule table merely because it
exists. But before excluding any table, inventory every market rule project and shared/common rule
project checked for this domain and classify every decision table. Shared/common rule projects are
not markets; keep them out of the per-market matrix and report them separately.

### Market Rule Project Inventory

| Market | Legacy decision-table project | Source `.decisiontable` count checked | Migrated rule impl count checked | Fixture count checked | Stale/non-authoritative source ignored? | Notes | Evidence confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `<market>` | `<path>` | `<count>` | `<count>` | `<count>` | `<yes/no/exception id>` | `<missing/extra assets>` | `<proven/inferred/not-found/open-question>` |

### Shared / Common Rule Project Inventory

Use this section when project conventions define shared/common rule projects or when a call path
reaches a non-market rule project. Do not represent these rows as market columns.

| Shared/common project | Source path | Decision-table count checked | Required/shared/unknown table count | Fixture location | Usage evidence | Evidence confidence |
| --- | --- | ---: | ---: | --- | --- | --- |
| `<project>` | `<path>` | `<count>` | `<count>` | `<path or gap>` | `<wrapper/project-name evidence>` | `<proven/inferred/not-found/open-question>` |

### Decision Table Classification

Classify every decision table found in the checked market rule projects and shared/common rule
projects. `unknown` blocks design. `domain-required` and `shared-required` must be carried into
design and migration for every applicable market or shared/common project.

| Decision table | Source scope | Markets/common projects present | Classification | Why this classification is correct | Direct source evidence | Required for this domain? | Exclusion / follow-up | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<table>` | `<market/shared-common/both>` | `<markets and/or common projects>` | `<domain-required/shared-required/used-by-other-domain/not-used-by-this-domain/unknown/excluded-with-approved-reason>` | `<reason>` | `<flow/rule/service paths>` | `<yes/no/blocker>` | `<approved exclusion or open question>` | `<proven/inferred/not-found/open-question>` |

### Domain Rule Usage Map

Map the domain's legacy call path to the rule tables it actually needs. Include direct business-rule
service calls and shared/transitive tables needed to interpret outputs such as event rules, peer
interfaces, config keys, reward/promotion identifiers, or error mappings.

For rule wrappers that target `DT/<DecisionTableName>`, prove the active rule project using the
wrapper namespace, explicit project-name pipeline value, or project-convention routing service. If a
same-named table exists in both market and shared/common projects, keep the evidence and fixture
paths separate.

| Operation / legacy service | Business-rule service or lookup | Active rule project evidence | Decision table | Markets/common projects required | Direct or shared/transitive | Inputs consumed | Outputs used by domain | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<operation/service>` | `<call*Rule/config lookup>` | `<namespace/project-name/routing evidence>` | `<table>` | `<markets/common projects>` | `<direct/shared-transitive>` | `<inputs>` | `<outputs>` | `<proven/inferred/not-found/open-question>` |

### Required Rule Asset Coverage

For every `domain-required` and `shared-required` table, prove coverage for every applicable market.
If a table is required but an asset or fixture is missing, record it as a blocker unless the human
reviewer explicitly approves a documented gap.

Include this source row-count matrix before coverage verdicts. Counts must come from legacy
`.decisiontable` rule rows, not another stale/non-authoritative source, the migrated rule
implementation, or repository `rules/`.

Market decision-table matrix:

| Decision table | `<market 1>` | `<market 2>` | `<market ...>` | Total |
| --- | ---: | ---: | ---: | ---: |
| `<table>` | `<count>` | `<count>` | `<count>` | `<total>` |

Shared/common decision-table matrix:

| Decision table | Shared/common project | Source row count | Fixture row count | Fixture path | Coverage verdict |
| --- | --- | ---: | ---: | --- | --- |
| `<table>` | `<project>` | `<count>` | `<count>` | `<path or gap>` | `<covered/partial/blocker>` |

| Market | Required DT count | Required rule impl count | Required source `.decisiontable` count | Required fixture count | Missing required tables/assets | Coverage verdict |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `<market>` | `<count>` | `<count>` | `<count>` | `<fixture file count and row count>` | `<table/asset gaps>` | `<covered/partial/blocker>` |

### Existing Rule Asset Verification

Use this only for migrated implementation assets already present under repository `rules/`.
Presence under `rules/` is not approval. Each candidate asset must be verified against the migration
process before design or coding may wire it.

| Rule table | Market | Candidate `rules/` asset | Compile/load evidence | Module/package routing | Model compatibility | Source reconciliation | Fixture/test reconciliation | Market isolation | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<table>` | `<market>` | `<path>` | `<pass/fail/not-run>` | `<pass/fail/gap>` | `<pass/fail/gap>` | `<source rows/actions/conditions reconciled or blocker>` | `<fixtures/tests reconciled or blocker>` | `<pass/fail/not-run>` | `<verified/verified-with-approved-gaps/blocker>` |

## Rules Detail

| Rule/config table | Used for | Legacy source | Migrated asset status | Fixture status | Evidence confidence |
| --- | --- | --- | --- | --- | --- |
| `<table>` | `<behavior>` | `<path>` | `<available/missing>` | `<available/missing>` | `<proven/inferred/not-found/open-question>` |

## Error Codes And Messages

Do not limit this section to directly hardcoded domain errors. Include every code discovered from
domain flows, invoked services, dependency fault mappings, dynamic propagated error fields, and
shared/common error translation tables that are part of this domain's error path. Codes that are
not proven reachable must still be mentioned and classified instead of omitted.

Usage classification values:

- `domain-direct` — the domain entry flow, utility, orchestration, branch, catch path, or wrapper
  sets or throws this code.
- `dependency-propagated` — the code is copied from a DAL/SOAP/REST/service fault or wrapper
  exception field.
- `shared-translation` — the code exists in an invoked shared/common error translation corpus, but
  direct domain emission is not proven.
- `domain-service-unused` — the code exists in relevant domain/service-family source but is not
  reachable from the traced operation call graph.
- `shared-unused` — the code exists in the invoked shared/common corpus but is not proven reachable
  from this domain.
- `unknown-reachability` — the code is relevant to checked sources/fixtures, but reachability cannot
  be proven from available source.

### Domain Error Inventory

| Code | Usage classification | Source | Condition / producer | Legacy message/details observed | Contract mapping | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `<code>` | `<domain-direct/dependency-propagated/domain-service-unused/unknown-reachability>` | `<flow/service/dependency>` | `<condition, catch path, or dynamic source field>` | `<message>` | `<reasonCode/status/body>` | `<proven/inferred/not-found/open-question>` |

### Shared/Common Error Translation Inventory

Include every code from invoked shared/common error translation tables. If the table is large,
keep this as a complete table or a complete generated appendix; do not summarize in a way that
hides individual codes.

| Code | Usage classification | Shared source / fixture | Translation condition | Error description | HTTP status | Reason | Output reason code | Domain reachability evidence | Evidence confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<code>` | `<shared-translation/shared-unused/unknown-reachability>` | `<decisiontable/fixture path>` | `<input errorCode or condition>` | `<errorDescription>` | `<httpErrorCode>` | `<reason>` | `<reasonCode>` | `<direct/propagated/not proven>` | `<proven/inferred/not-found/open-question>` |

### Error Inventory Gaps

- Sources checked for codes:
- Codes found but not mapped:
- Codes with dynamic values where finite enumeration is impossible:
- Human decisions needed:

## Golden Fixtures

Generated fixtures present:

- `<path>`

SME-validated fixtures:

- `<path or none yet>`

Candidate fixtures generated from source `.decisiontable`:

| Decision table | Required markets | Candidate fixture path pattern | Source parser / command | Generation status | SME validation status |
| --- | --- | --- | --- | --- | --- |
| `<table>` | `<markets>` | `tests/parity-data/rules/<DecisionTable>/<Market>.json` | `<command>` | `<generated / failed / not-run>` | `<validated / pending / blocker>` |

Rule parity fixture coverage for decision-table-backed behavior:

| Decision table | Market | Committed fixture | Source rule count | Fixture rule count | Validation status |
| --- | --- | --- | --- | --- | --- |
| `<table>` | `<market>` | `tests/parity-data/rules/<DecisionTable>/<Market>.json` | `<count>` | `<count>` | `<validated / corrected / blocker>` |

Source decision-table evidence reviewed:

- Source artifacts:
  - `<source decision-table path from migration conventions>/<table>.decisiontable>`
- Validation corrections:
  - `<correction or none>`
- Stale/non-authoritative source handling:
  - `<ignored / named human-approved exception>`

Fixture blockers:

- `<fixture scenario and reason>`

## Decision-Table-To-Target Conversion Fidelity Audit

Required for every decision table whose migrated or generated rule implementation may be used by
design or coding. If no rule implementation exists yet, state that and mark the table as a
design/migrate blocker or approved gap. Legacy rule-extraction artifacts that project conventions
mark stale or non-authoritative must not appear as the source unless a numbered human-approved
exception is recorded. Repository migrated rule asset paths must not appear as source
decision-table evidence; they may appear only in the rule asset column.

| Decision table | Market | Source decision table | Rule asset | Fixture/test evidence | Row/rule/test reconciliation | Helper/operator coverage | Conflict/overwrite audit | Activation semantics | Implementation-shape evidence | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<table>` | `<market>` | `<path>` | `<path or missing>` | `<fixture/test path>` | `<source=N fixture=N impl=N tests=N or exclusions>` | `<all translated / blockers>` | `<none / duplicate inputs / broad overwrite>` | `<independent / sequential / first-match / unknown>` | `<compile/load, module/package, market-isolation verdict>` | `<pass / pass-with-exclusions / blocker>` |

Conversion blockers:

- `<table/market/rule ids, source path, lost condition/action/helper/order behavior, impact, owner>`

Potential future fixture scenarios:

- `<case>`

## Design And Code Handoff

This characterization is not the target design and is not authorization to code. It is the input
that the design phase converts into the target migration design. After design approval, the migrate
phase uses the approved design to implement code and tests.

### Characterization To Design Traceability

| Characterization input | Design must decide / specify | Code must later implement |
| --- | --- | --- |
| Operation inventory and contract inputs | Controller methods, exact paths, params, headers, DTOs, status/body rules | Contract-conformant endpoints |
| Service signatures and pipeline schema | Internal command/service model replacing WebMethods pipeline docs | Request normalization and context model |
| Pipeline variable lineage | Ordered orchestration and carried values | Service sequence preserving producer/consumer order |
| MAP-node field renames | DTO/rule/DAL/exception mapping table | Explicit mapper/service assignments |
| Branch logic | Branch matrix and expected outcomes | Conditionals and branch tests |
| Dependency behavior register | Target replacement and failure mapping for each dependency | DAL/downstream/rule clients |
| Functional config and reference data | Target source for behavior-affecting config, secret handling, env/tenant/market variance, defaults/fallbacks, and failure behavior | Spring configuration properties, secret references, DAL/reference-data calls, or approved static values plus tests |
| Side effects and atomic write boundaries | Write/read boundary, logging, rollback/partial failure behavior | Atomic write and side-effect handling |
| Data operations | Target data-layer endpoints and parameters | DAL client methods |
| Rules and conversion fidelity | Audited rule implementations/model classes, market isolation, and conversion-remediation work packages | Rule wiring and rules parity tests only for audited assets |
| Error codes/messages | Complete direct, propagated, shared/common, unused, and unknown-reachability error inventory; public error body/status mapping | Exception mapper / response builder plus tests for direct and propagated/shared mappings |
| Golden fixture gaps | Fixture plan | Rule/API parity test data after gates allow it |
| Existing target implementation baseline | Reuse/refactor/replace/defer decisions and remediation work packages | Code changes only after design classifies existing files/assets and resolves mismatches |

### Design Phase Minimum Output

- Public API shape:
- Internal orchestration:
- DTO and field mapping:
- Dependency plan:
- Functional config / reference-data plan:
- Rule plan:
- Branch plan:
- Error mapping:
- Test and fixture plan:

### Migrate Phase Minimum Output

- Contract-conformant controller and DTOs.
- Service orchestration matching the approved call sequence and branch matrix.
- Rule integration with market isolation.
- Data/downstream clients through approved boundaries.
- Unit tests for mapping and branch behavior.
- Rule parity tests and fixtures for approved scope.
- API parity tests and fixtures after deploy-boundary prerequisites are met.

## Open Questions / Decisions Required

Each open question must include impact, options, recommendation, owner, and required phase before
resolution. Do not leave questions embedded only in prose. Every `open-question` confidence marker
must link to one numbered item here or to a listed human-approved decision.

### SME Decision Summary

| ID | Decision needed | Why SME/source-owner decision is required | Recommendation | Required before |
| --- | --- | --- | --- | --- |
| `Q-001` | `<decision>` | `<impact/risk>` | `<recommended option>` | `<design/migrate/gate>` |

### Numbered Questions

1. `Q-001: <Question title>`
   - Impact:
   - Options:
   - Recommendation:
   - Owner:
   - Required before:
   - Evidence confidence: `open-question`

## Analyze Gate Readiness

State whether the artifact is ready for human review and whether it is ready for analyze-phase
approval. If not approval-ready, list the blocking open questions.
