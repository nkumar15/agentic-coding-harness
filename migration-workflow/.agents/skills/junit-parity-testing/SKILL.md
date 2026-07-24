---
name: junit-parity-testing
description: Write JUnit 5 tests for a legacy-to-new migration — unit tests per layer, characterization tests derived from legacy rule definitions, recorded-replay API parity, and tenant-isolation guards. Generic and reusable across migrations. Use when writing or evaluating tests that prove the new system matches legacy behavior.
license: Proprietary
metadata:
  author: Neeraj
  version: "2.0"
---

# JUnit & Parity Testing

Reusable approach for proving a migrated component behaves identically to the legacy one. This
skill is the generic "how". Concrete facts — where the legacy golden data comes from, the legacy
API fixtures live, the deployed new API base-URL env var, and the build's test-tag command — are
supplied by the calling agent.

**Core principle:** the only meaningful validation is *same input to legacy and new, compare
outputs*. Mocking hides bugs — it tests your assumptions, not reality. Minimize mocking; maximize
real comparison.

For a human-readable test plan and per-work-package checklist, read
`references/testing-strategy.md` when designing, implementing, or reviewing migration tests.

---

## Three test levels

### 1. Unit tests (per layer)
Standard JUnit 5 for controllers (header/param validation, status codes), services (orchestration
logic), and DTO mapping. Fast; run on every build.

### 2. Characterization tests (from legacy rule definitions) — the golden data
Legacy decision-table rows are input/output pairs that define what production does today.
Auto-derive tests from them rather than hand-writing assertions:
1. Parse each rule row: conditions → inputs, actions → expected outputs.
2. Generate one parameterized JUnit case per row that exercises the new logic and asserts the
   output equals the row's expected output.
3. Before execution, validate fixture integrity:
   - no two rows have identical normalized inputs with different expected outputs unless the source
     table has explicit ordering/first-match semantics and the test models that behavior;
   - every source row maps to one fixture case, one executable rule path, and one assertion;
   - skipped rows and tenants are reported as blockers unless an approved exclusion exists.
4. Tag them so the parity gate suite picks them up.

```java
@Tag("parity")
@ParameterizedTest
@MethodSource("goldenRows")            // generated from the legacy rule source
void matchesLegacy(GoldenRow row) {
    Result result = engine.evaluate(row.toRequest());
    assertEquals(row.expected("category"), result.getCategory());
}
```
This guarantees every legacy rule has a corresponding passing test — the completeness check
hand-written tests can't give.

Contradictory generated tests are not proof that the implementation is wrong. They usually mean the
fixture or rule conversion lost a discriminator, helper function, or row ordering rule. Classify that
as fixture/conversion loss and send it back to characterization or conversion tooling before coding
continues.

### 3. Recorded API-diff parity — the authoritative check
Parity is ultimately proven by replaying a **captured legacy request/response fixture** against the
deployed new API and diffing the new response against the captured legacy response field-by-field.
- Legacy API access may happen outside this repository as a one-time capture exercise; do not
  require direct legacy API access during normal gate execution.
- Store captured fixtures under the project-defined parity-data location.
- Drive inputs from contract examples, legacy captures, and characterized edge/failure cases.
- Diff the FULL response field-by-field; ignore only documented volatile fields or intentional
  contract fixes.
- Any unexplained diff fails parity.
- Gate these tests on the new deployed API base URL being set; skip-with-loud-log is not a pass.

Until API fixtures and a deployed new endpoint are available, level 2 + contract examples are the
baseline. The test report MUST state which mode is in effect (recorded API parity vs
characterization-only).

## Tenant-isolation guard

A required parity guard in multi-tenant systems: assert one tenant's rules do NOT fire for another.
```java
@Tag("parity")
@Test
void tenantARulesDoNotFireForTenantB() {
    Result r = engine.evaluate(sameInputButTenant("B"));
    assertNotEquals("A-specific-output", r.getCategory());
}
```

## The parity gate suite

A gate runs the tagged parity suite (e.g. a tagged test run via the build tool). It passes only
when every characterization + isolation (+ recorded API replay, when enabled) test is green. The gate's
verifier runs it and reports; it never fixes — failures route back to the implementer.

## Coverage expectations

- Every contract operation: happy path + required-header/param negative cases.
- Every SOAP/REST downstream client: exact endpoint config, protocol shape, headers/auth,
  namespace/localPart or method/path, schemaVersion/action, request fields, response fields, and
  fault/error mapping derived from approved contract evidence.
- Every migrated rule: one characterization case (auto-generated).
- Every generated fixture set: duplicate-input/conflicting-output validation.
- Every unit of work: the tenant-isolation guard.
- Multi-step/atomic operations: a test covering the rollback path.

## Don't

- Don't mock the engine under test in parity tests — exercise the real logic.
- Don't assert on a subset of fields when the contract promises more — diff the full response.
- Don't silently skip a tenant/rule — a skipped parity test reads as "covered" when it isn't; log it.
