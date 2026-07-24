# Feature Verification

Feature work must carry a verification thread from PRD to architecture to development. The global
`checks_green` gate proves the repository is generally green; `feature_verification` proves the
specific feature is safe to merge.

## PRD Requirements

Every feature PRD must include a `Verification Requirements` section that states:

- user-visible acceptance checks for each user story
- expected unit, integration, contract, migration, seed, UI, or smoke coverage as applicable
- local commands a developer should run for the feature
- test data, fixture, or seed-data expectations
- explicit non-goals for baseline, evaluation, performance, or deployment artifacts when those are
  separate work

The PRD should describe required confidence, not implementation design.

## Architecture Requirements

Every feature architecture document must include a `Verification Strategy` section that maps PRD
requirements to concrete checks:

- test files to add or update
- integration tests for stateful or boundary behavior
- contract or smoke tests for critical runtime behavior
- migration and rollback checks for schema changes
- seed or fixture checks when data changes
- UI build or interaction checks for frontend changes
- exact local commands from `.agents/rules/project-conventions.md`

## Development Requirements

The development phase must implement the approved verification strategy. If implementation differs
from the strategy, update the architecture or flag the mismatch before coding.

Feature development is not complete until changed behavior has focused tests, required commands have
run, and verification evidence is recorded in the project-defined location.

## Verifier Requirements

The verifier evaluates:

- `checks_green`: run every global command listed in `.agents/process/gates.yaml`
- `feature_verification`: confirm the feature-specific verification strategy was satisfied

Do not treat a passing global suite as sufficient when the feature-specific verification plan is
absent, unclear, or incomplete.
