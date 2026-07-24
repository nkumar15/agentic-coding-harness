# Migration Testing Strategy

Use this reference when designing, implementing, or reviewing migration tests. The goal is not raw
coverage; the goal is proving the Spring Boot behavior matches the contract and characterized
legacy behavior.

## Test Layers

| Layer | Purpose | Typical Owner | Gate |
| --- | --- | --- | --- |
| Unit tests | Verify DTO mapping, service orchestration, branch behavior, error mapping, DAL client request construction, and rule facade behavior in isolation for the active domain. | `springboot-migrator` | `domain_migration_checks_green` |
| Contract tests | Verify generated Spring API shape matches the contract declared in project conventions for the active domain. | `api-contract-verifier` reports; migrator fixes | `contract_verified` |
| Rules parity tests | Feed curated legacy decision-table fixture rows into the migrated rule implementation and compare outputs for the active domain, including market isolation. | `legacy-parity-verifier` reports; migrator or analyze fixes by cause | `rules_parity_verified` |
| Cross-domain regression | Run the full reactor and prove the active domain introduced no new failures beyond approved WIP baseline waivers. | `springboot-migration-verifier` reports; migrator fixes code-caused failures | `cross_domain_regression_green` |
| Local app health smoke | Start the assembled Spring Boot app through the project-declared local runtime and verify actuator health. | `springboot-migration-verifier` reports; migrator fixes startup/config/packaging failures | `springboot_app_health_checked` |
| API parity tests | Replay captured legacy API requests against deployed Spring Boot API and diff full responses. | `legacy-parity-verifier` reports; owner depends on cause | `api_parity_verified` |
| Code review checks | Confirm tests cover the approved design and no critical scope is unverified. | `springboot-migration-reviewer` | `migration_review_approved` |

## Analyze To Test Mapping

| Characterization Evidence | Required Test Obligation |
| --- | --- |
| Contract operation and required headers/params | Contract test and controller validation/negative tests |
| Service signature field, optionality, nested doc/list | DTO serialization/deserialization or service mapping test |
| Pipeline variable lineage or field-mapping-step rename | Service mapper/unit test proving source-to-target value |
| Branch or loop | Unit test per branch/loop outcome |
| Dependency failure mapping | Unit or integration-style test with failed DAL/client response |
| SOAP/REST downstream contract evidence | Client contract test asserting endpoint config, namespace/localPart or method/path, schemaVersion/action, request/response/fault mapping, and headers/auth |
| Runtime config / packaging / health-probe change | Local app health smoke plus Helm/deployment evidence |
| Error-code inventory | Tests for direct domain codes, dependency-propagated codes, shared/common translation mappings, and explicit approved exclusions or gaps |
| Side effect or atomic write boundary | Service test for order/rollback/partial-failure behavior, plus API parity scenario where available |
| Legacy decision-table row | Rules parity fixture/test row |
| Market-specific rule behavior | Rules parity by market plus cross-market isolation guard |
| Legacy API example | API parity recorded-replay fixture |

## Per Work Package Checklist

- [ ] Happy path for the implemented operation/slice.
- [ ] Required header/param/body validation.
- [ ] Null, blank, absent, empty-list, and boundary cases proven by characterization.
- [ ] Field renames and pipeline-derived mapping.
- [ ] Branch-specific behavior.
- [ ] Dependency failure and error body/status mapping.
- [ ] SOAP/REST downstream client contract when a peer dependency is touched: exact URL/config
      source, namespace/localPart or method/path, schemaVersion/action, request fields, response
      mapping, fault mapping, and propagated headers/auth.
- [ ] Complete error-code inventory coverage for codes in the active work package: direct,
      propagated, shared/common translation, intentionally excluded, and unknown-reachability gaps.
- [ ] Header/legal-entity/request-id propagation to DAL or downstream client.
- [ ] Rule invocation inputs/outputs and market isolation when rules are touched.
- [ ] Side-effect ordering, atomic write boundary, rollback/compensation, or idempotency when touched.
- [ ] Local app health gate impact considered when startup, packaging, config binding, rules
      loading, or local dependencies are touched.
- [ ] Helm/deployment impact considered when env vars, secrets, ports, probes, downstream URLs, or
      service exposure are touched.
- [ ] No skipped test is counted as a pass; every skip has an owner, reason, and gate impact.

## Rules Parity Requirements

- Fixture files under the project-declared rules fixture path are the parity contract. A common
  pattern is `tests/parity-data/rules/<DecisionTable>/<TenantOrMarket>.json`.
- Fixtures must be derived from the authoritative legacy decision-table artifacts named in the
  project migration conventions, not repository `rules/` migrated assets or another
  stale/non-authoritative source.
- Candidate fixture data and the per-market source rule-count matrix should be generated during
  characterization with the project-approved parser declared in migration conventions, then
  validated/corrected before being treated as approved golden fixtures.
- Candidate parser output from a source that project conventions mark stale or disallowed is not
  valid parity input unless a human explicitly approved a named exception.
- Expected, generated, ran, passed, failed, and skipped counts must reconcile.
- Every `domain-required` and `shared-required` table must have fixture coverage for every
  applicable market, with one file per decision-table/market pair, or an approved documented gap.
- Duplicate normalized inputs with conflicting outputs, unsupported helper/operator translations,
  broad-overwrite risks, or missing market scope block parity until classified.
- Existing rule assets under repository `rules/` must have migration-process verification before
  they are counted as valid parity targets: compile/load or build success, module/package routing,
  model compatibility, source/fixture/test reconciliation, and market isolation.
- Cross-market isolation must prove one market's rules do not fire for another legal entity.
- The parity verifier saves the gate result, coverage counts, failures, gaps, and verdict to
  `.analysis/<domain>/<domain>-rules-parity-report.md`.

## API Parity Requirements

- API parity runs only against the deployed Spring Boot API with the live API base URL env var
  declared in project conventions set.
- Fixtures live under `tests/parity-data/api/<domain>/`.
- Each fixture should contain the captured legacy request, expected legacy response, normalization
  rules for volatile fields, and data-state assumptions.
- Diff full responses field-by-field after documented normalization; do not assert only a subset.
- Classify failures as code bug, data drift, fixture error, conversion loss, env/config, or
  missing rule implementation. Only code bugs route directly to implementation fixes.
- The parity verifier saves the gate result, coverage counts, failures, gaps, and verdict to
  `.analysis/<domain>/<domain>-api-parity-report.md`.

## Local App Health Requirements

- Local app health is an offline gate, separate from API parity. It proves the packaged app can
  start locally and answer the configured actuator health endpoint.
- Run the commands declared for `springboot_app_health_checked` in `gates.yaml`; do not substitute
  a bare Maven or IDE run when the project declares a container runtime.
- Record the local runtime, service status, health URL/response, logs on failure, and any
  human-approved runtime override in the implementation verification report.
- Health failures are classified separately from API parity: code/config/packaging/dependency/env.
  Code/config/packaging failures route to the migrator; missing local runtime or external env gaps
  need explicit owner/action.

## Coverage Expectations

- Every contract operation has happy-path and required-header/param negative coverage.
- Every characterized branch has at least one test or an approved documented gap.
- Every characterized error-code category has coverage or an approved documented gap; tests must not
  cover only directly thrown codes when the design includes propagated/shared translation behavior.
- Every touched SOAP/REST peer dependency has a client contract test proving the exact wire shape,
  not just a mocked success response.
- Every migrated decision-table row has rules parity coverage unless explicitly excluded with human
  approval.
- Every generated fixture set has duplicate/conflict validation.
- Every multi-step write has atomicity/partial-failure coverage where the behavior is in scope.
- Every market-specific rule path has market-isolation coverage.
- Every migration checkpoint proves the app still starts locally and health probes are aligned with
  deployment assets, or records an explicit approved gap.

## Review Questions

- Did the tests prove the approved architecture, or only compile the implementation?
- Is every `WP-*` linked to tests in the progress artifact?
- Are any gates passing because tests silently skipped or asserted too little?
- Are parity failures routed by cause instead of automatically treated as code bugs?
- Is any untested behavior a documented risk accepted by the human reviewer?
