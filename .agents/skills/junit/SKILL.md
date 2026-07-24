---
name: junit
description: Write and evaluate Java JUnit 5 tests for feature, bug, and maintenance work. Use when a consuming repository's project conventions declare JUnit or Java test coverage.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "1.0"
---

# JUnit Testing Skill

Use this skill when `.agents/rules/project-conventions.md` says the project uses Java with JUnit.
Project conventions define Java version, build tool, module layout, test source roots, test naming,
test tags, and exact commands.

## Test Scope

- Add or update tests in the same module as the behavior change unless project conventions say
  otherwise.
- Prefer focused unit tests for pure logic, service orchestration, DTO mapping, validation, and
  error translation.
- Add Spring MVC or WebFlux slice tests for controller request/response behavior.
- Add integration tests only when wiring, persistence, messaging, transactions, or framework
  configuration is part of the change.
- For migrations or legacy parity, use `junit-parity-testing` instead of this generic feature
  testing skill.

## JUnit 5 Practices

- Use JUnit Jupiter APIs and the assertion style already used by the project.
- Keep test names behavior-oriented and specific.
- Cover success paths, validation failures, dependency failures, boundary values, and security or
  tenant checks that the changed behavior depends on.
- Avoid overspecified assertions on unrelated fields or implementation details.
- Keep mocks at architectural boundaries. Do not mock the class under test.
- Use parameterized tests when multiple inputs exercise the same rule.
- Reset shared state between tests; tests must be order-independent.

## Spring Boot Tests

- Use the narrowest useful Spring test slice: controller tests for HTTP surface, data tests for
  persistence, and full context tests only when configuration or cross-bean wiring is the subject.
- Verify HTTP method, path, headers, query params, status codes, error bodies, and JSON field names
  against the project contract.
- For `RestTemplate`, WebClient, SOAP, or peer-service clients, test the exact outbound method,
  path/template, headers, request body, response mapping, and non-2xx behavior.
- Prefer test fixtures/builders that make required fields explicit without hiding behavior.

## Verification

- Run the module-specific JUnit command declared in project conventions.
- If a full build is too expensive for the phase, run the focused module tests first and state which
  broader command remains.
- Report skipped or blocked tests with the exact missing command, dependency, fixture, or
  environment variable.

## Don't

- Don't add tests that only assert mocks were called unless the interaction is the behavior.
- Don't change production code only to make it easier to test without an approved design reason.
- Don't silently weaken existing assertions or disable tests.
