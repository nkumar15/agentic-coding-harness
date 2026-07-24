---
name: java-springboot
description: Write Spring Boot (Java 17) backend code — REST controllers, request/response DTOs, a service layer, RestTemplate clients to a downstream data/API service, exception handling, and env-based config. Generic and reusable across Spring Boot projects. Use when implementing or changing Spring Boot endpoints, DTOs, services, or downstream clients.
license: Proprietary
metadata:
  author: Neeraj
  version: "2.0"
---

# Spring Boot Backend

Reusable patterns for a Spring Boot REST service or backend module. This skill is the generic
"how". Concrete project facts — the API contract, base path, header/param constant classes,
downstream service URLs, package names — are supplied by the calling agent; do not hardcode them
here.

When a contract (OpenAPI/Swagger) exists, treat it as authoritative: every path, param, header,
field name, type, and status code must match it exactly. Never invent or rename contract fields.

For migrate-phase implementation, read `references/migration-implementation-checklist.md` and apply
it per approved work package. Architecture/design traceability belongs to the `migration-design`
skill.

---

## Module layout (per domain)

```
{module}/src/main/java/{base-package}/{domain}/
  {Domain}Controller.java   # REST surface — thin
  {Domain}Service.java      # orchestration + business logic
  {Domain}DalClient.java    # RestTemplate calls to the downstream service
  dto/                      # request + response DTOs matching the contract
```
Keep shared DTOs/constants/exceptions in a shared core module.

## Controllers

- `@RestController` + `@RequestMapping(BASE_PATH)`.
- One method per contract operation; HTTP method + path **exactly** as the contract specifies.
- Declare required headers with `@RequestHeader`, and params with `@RequestParam` — reference
  name constants (don't inline string literals for header/param names that must match a contract).
- Thin body: validate required params, call the service, return `ResponseEntity`.
- Add springdoc annotations (`@Operation(operationId=...)`, `@ApiResponse` per status code).

```java
@GetMapping("/widget")
@Operation(operationId = "queryWidget", security = @SecurityRequirement(name = "Authorization"))
public ResponseEntity<?> queryWidget(
        @RequestHeader(HEADER_AUTHORIZATION) String authorization,
        @RequestHeader(HEADER_REQUEST_ID) String requestId,
        @RequestHeader(HEADER_TENANT_ID) String tenantId,
        @RequestParam(PARAM_CODE) String code, ...) {
    try {
        return ResponseEntity.ok(widgetService.query(code, ..., tenantId, requestId));
    } catch (RestClientException e) {
        return ResponseEntity.badRequest().body(new ErrorResponse("400", "Bad Request", e.getMessage()));
    } catch (Exception e) {
        return ResponseEntity.internalServerError().body(new ErrorResponse("500", "Internal Error", e.getMessage()));
    }
}
```

## DTOs

- Separate request and response DTOs per operation. Field names match the contract EXACTLY — use
  `@JsonProperty` when the JSON name isn't a valid Java identifier (e.g. hyphenated names).
- Mirror the contract's schema types precisely; don't widen/narrow.
- Plain data carriers — no logic.

## Services

- Hold the orchestration: the ordered downstream calls, any rules-engine invocation, and the
  field mapping/renames between downstream shapes and the contract response.
- Receive validated primitives from the controller; return a response DTO.
- When migrating, replicate the legacy call **sequence and field mapping** exactly — this is where
  behavioral parity is won.
- Pass tenant id and correlation id through to downstream calls for routing + tracing.
- Implement behavior-affecting config/reference-data decisions exactly as approved by migration
  design. If a branch, downstream URL, rule input, error mapping, threshold, or market/peer
  mapping comes from config, keep that dependency visible in the service/config layer and cover it
  with tests.

## Downstream client (RestTemplate)

- A thin `{Domain}DalClient` using `RestTemplate`. Keep it pure transport.
- Propagate correlation and tenant headers on every call.
- Let `RestClientException` propagate to the service/controller (mapped to 4xx/5xx there).
- Do field renames/reshaping in the **service layer**, not the client — keep renames visible/testable.
- For multi-step writes, use the downstream's atomic endpoints rather than emulating an
  atomic write with several calls.

```java
public WidgetResponse getWidget(String id, String tenantId, String requestId) {
    HttpHeaders h = new HttpHeaders();
    h.set(HEADER_REQUEST_ID, requestId);
    h.set(HEADER_TENANT_ID, tenantId);
    return restTemplate.exchange(baseUrl + "/widget?id={id}", HttpMethod.GET,
        new HttpEntity<>(h), WidgetResponse.class, id).getBody();
}
```

## Downstream protocol contracts

- Implement downstream clients from the approved design's contract evidence, not from an example
  payload or guessed endpoint shape.
- Keep environment-specific hosts and base URLs in configuration, but keep protocol/schema
  constants such as SOAP namespace, root localPart, schemaVersion, SOAPAction, REST method, and
  path template tied to WSDL/XSD/source evidence.
- For SOAP clients, prefer typed/generated clients or `WebServiceTemplate` when the project uses
  them. If a module hand-builds XML, centralize the namespace/root/schema constants and unit-test
  the exact outbound envelope, including namespace, localPart, schemaVersion shape/value, request
  fields, content type, and fault/no-match mapping.
- For REST peer clients, unit-test the exact method, path template, query params, headers, request
  body, response mapping, and non-2xx mapping.
- Do not treat a successful network route as contract proof; a peer service can be reachable while
  rejecting the payload because the namespace, root element, schemaVersion, method, or path is
  wrong.

## Error handling

- Use a single structured error response type (code, message, detail) from the shared core module.
- Register/replicate consistent error codes and messages. When migrating, reproduce the legacy
  error codes/messages exactly — consumers may parse the message text, not just the status code.
- When an approved migration design supplies an error-code inventory, implement from that inventory
  without narrowing it to direct local exceptions. Preserve the design's classifications for
  direct domain codes, dependency-propagated codes, shared/common translation mappings, intentional
  exclusions, and unknown-reachability gaps.

## Logging

- Use standard Spring Boot application logging practices. Prefer SLF4J with
  `private static final Logger LOGGER = LoggerFactory.getLogger(CurrentClass.class);` unless the
  target module already has a stronger local convention.
- Add logs only at useful operational boundaries: downstream dependency failures, retries/fallbacks,
  ignored legacy-equivalent exceptions, side-effect/write decisions, and rule/branch outcomes that
  are needed to diagnose parity or production behavior.
- Do not add boilerplate method entry/exit logs, DTO logs, or duplicate exception logs at every
  layer. Prefer one clear log at the layer that owns the decision or at the centralized exception
  handler.
- Use levels deliberately: `debug` for diagnostic rule/branch/parity details and suppressed
  recoverable exceptions, `info` only for meaningful lifecycle/business milestones already used by
  the project, `warn` for recoverable anomalies or fallback behavior, and `error` when an operation
  cannot complete or a dependency failure is propagated.
- Use parameterized messages (`LOGGER.debug("Rule {} skipped for tenant {}", ruleName, tenantId)`)
  instead of string concatenation. Guard with `isDebugEnabled()` only when preparing the log arguments
  is expensive.
- Never log secrets, authorization tokens, full request/response bodies, or personal/health data.
  Include correlation/request id, tenant/legal-entity id, operation name, and safe business keys only
  when they are already approved for logs.

## Config

- All external URLs and secrets via environment variables. Never hardcode hosts.
- Secret-backed values come from the platform's secret store (e.g. k8s Secrets) — never commit secrets.
- For migration work, use the approved architecture's Functional Config And Reference Data Design
  as the source of truth. Implement each behavior-affecting config value through the approved target
  source: Spring configuration property, secret-backed property, application config,
  DAL/reference-data endpoint, fixture-backed test data, or explicitly approved static reference
  value.
- Prefer typed Spring configuration (`@ConfigurationProperties`) for grouped non-secret settings
  when the target module needs more than one related value. Keep single downstream base URLs simple
  if the existing module convention already uses `@Value`.
- Validate required config at startup or at the service boundary as approved by design. Preserve the
  design's default/fallback/missing-value behavior instead of inventing a safer-looking default.
- Do not copy legacy runtime config file values into Java constants unless the approved design
  explicitly classifies them as static reference data.
- Tests must cover config-driven branches, defaults, missing-value behavior, and env/tenant/market
  variance that the approved design marks in scope.

## Runtime Health

- When a Spring Boot change affects runtime wiring, configuration, dependency injection, generated
  resources, or deployment packaging, the assembled application should start through the project's
  declared local runtime and respond healthy on its configured actuator health endpoint.
- Treat startup failures as implementation evidence, not as optional manual testing. Common causes
  include constructor injection ambiguity, missing configuration binding, resource packaging gaps,
  invalid rule assets, missing downstream-local dependencies, or incorrect profile/env wiring.
- Use the health-check gate and local runtime commands supplied by the calling project. Do not
  invent Maven/IDE startup commands when the project declares a container/runtime path.
- For migration work, record the resolved local-runtime command, health URL, result, and any
  approved runtime override in the implementation verification report and progress artifact.

## Deployment / Helm

- When implementation changes runtime behavior, keep deployment assets in sync. Examples include
  new or renamed environment variables, secret-backed properties, service ports, context paths,
  actuator health paths, liveness/readiness probes, downstream service URLs, resource requirements,
  image/startup commands, ingress/service exposure, and sidecar/proxy assumptions.
- Use the project conventions and approved architecture to locate the target chart and values
  files. Update base values, environment overlays, and secret-placeholder files as needed, but never
  commit real secrets.
- Health probes in deployment assets must match the app's actual actuator endpoints and management
  exposure. If the design requires a new dependency or config value, the chart must expose it in the
  same implementation checkpoint unless the design records a deploy-owner gap.
- If a work package has no Helm/deployment impact, record that explicitly in the progress and
  implementation verification artifacts so reviewers know it was checked.

## Don't

- Don't bypass the downstream service to reach a database or peer service directly.
- Don't invent fields or rename contract fields.
- Don't put business logic in controllers or DTOs.
- Don't add speculative abstraction/config that wasn't asked for.
