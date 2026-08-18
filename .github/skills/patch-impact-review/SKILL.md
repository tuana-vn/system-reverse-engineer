---
name: patch-impact-review
description: Review a patch or Git diff against the evidence-backed current-system baseline, trace impact from changed code through externally observable contracts and runtime dependencies, identify compatibility/regression risks, and derive evidence-backed test viewpoints, behavior matrices, and expected results.
license: MIT
---

# Patch Impact Review V2 — Contract + Runtime + Test Impact

## Purpose

A patch impact review is NOT a changed-function inventory.

The review must determine:

```text
PATCHED CODE
→ affected runtime behavior
→ affected externally observable contract
→ affected integration/data/state contract
→ compatibility/regression risk
→ required verification
```

A changed method is only the starting point.

## Baseline Safety

A patch is proposed behavior until independently verified as merged/current behavior.

- Do not update canonical reverse-engineering memory from the patch alone.
- Use CURRENT SOURCE as authority for baseline behavior.
- Use the patch/diff as candidate future behavior.
- Use requirements/specifications as intended behavior.
- If requirement, source, and patch disagree, show the disagreement explicitly.

## Inputs

Use all applicable inputs:

- patch / Git diff
- current source
- promoted reverse-engineering baseline
- requirement / issue / customer clarification
- API specification / OpenAPI / annotations / controllers
- tests and fixtures
- integration protocol definitions
- configuration and persistence schema

Do not require every input to exist. Record evidence gaps instead of guessing.

# 1. Reconstruct the Change at Three Levels

## 1.1 Business Purpose

Why the change is needed.

## 1.2 Observable Functional Behavior

What a caller, API consumer, operator, external system, or persisted state can observe before vs after.

For a bug fix:

```text
Observed / Reported Problem
→ PATCH-IMPLIED ROOT CAUSE
→ Changed Rule
→ Corrected Observable Behavior
```

Label patch-implied root cause unless independently source-verified.

## 1.3 Technical Implementation

How the patch implements the behavior:

- changed files
- classes/functions/methods
- conditions/branches
- data transformations
- integrations
- configuration/state changes

# 2. Mandatory Impact-Surface Discovery

For EVERY semantically changed behavior, trace both directions:

```text
UPSTREAM / EXPOSURE TRACE
changed symbol
← callers
← service/facade/handler
← controller/resource/router
← external endpoint/event/job/CLI entry point

DOWNSTREAM / EFFECT TRACE
changed symbol
→ callees/utilities
→ external client/DB/message/config/file
→ response/state/side effect
```

Stop only when the behavior is classified as one of:

```text
EXTERNALLY_EXPOSED
INTERNAL_ONLY
BACKGROUND_OR_SCHEDULED
EXTERNAL_INTEGRATION_ONLY
SOURCE_NOT_RESOLVED
```

Do NOT stop at the first caller or callee.

# 3. REST / HTTP API Contract Impact — Mandatory When Reachable

If any changed behavior is reachable from REST/HTTP, identify the exact affected API surface.

For each affected endpoint inspect:

## Endpoint identity

- API/version
- HTTP method
- route/path
- controller/resource/handler method
- applicable media types

## Request contract

- path parameters
- query parameters
- headers
- cookies if applicable
- request body schema
- nested body fields
- required/optional status
- nullability
- defaults
- allowed values/enums
- ranges/length/format
- cross-field / parameter-combination rules
- conditional requirements

## Response contract

- HTTP status codes
- response body/schema
- fields added/removed/changed
- field type/format changes
- conditional field presence
- null vs omitted behavior
- response headers
- ordering/pagination/filtering where relevant

## Error contract

- validation errors
- domain errors
- external integration errors
- error code/message mapping
- HTTP status mapping

## Compatibility contract

Check explicitly:

- old request still valid?
- old request produces same result?
- new parameter changes default behavior?
- parameter omitted vs null vs empty?
- old clients can parse new response?
- previously returned fields removed/renamed/retyped?
- new validation rejects previously valid requests?
- default path invokes more expensive downstream behavior?

If no REST endpoint is affected, state `NO_DIRECT_REST_API_IMPACT` and provide the source trace proving why.

# 4. Non-REST Contract Impact

Inspect all applicable boundaries:

- CLI command/options
- RMI/RPC
- external SDK/API calls
- database schema/query/keys
- message/event schema and topic/queue
- files/configuration generated or consumed
- cache keys
- scheduled jobs/batch inputs
- authentication/authorization inputs
- logs/audit/metrics where behaviorally significant

For each boundary identify:

```text
input → transformation → output / side effect → failure behavior
```

# 5. Data and State Impact

Trace changed values through their lifecycle.

Check:

- parsing
- validation
- normalization
- conversion
- storage/persistence
- comparison/equality
- map/cache keys
- serialization/deserialization
- response mapping
- external-command construction
- configuration generation
- logging/display

For identifier-like values additionally check:

- prefix/range/length assumptions
- numeric/string conversion
- arithmetic
- truncation/padding
- uniqueness/collision
- backward-compatible lookup

# 6. Compatibility and Regression Impact

Evaluate separately:

## Functional compatibility

Existing behavior remains valid unless intentionally changed.

## API compatibility

Request and response contract compatibility.

## Integration compatibility

External command/API/protocol compatibility.

## Data compatibility

Old persisted/configured/cached values remain usable.

## Performance compatibility

Check whether the patch changes:

- number of external calls
- amount of data requested/returned
- more expensive command options/query modes
- loops/retries
- cache behavior
- database query shape

## Security compatibility

Check authorization/validation/input exposure only when the changed path intersects them.

# 7. Mandatory Behavior Matrix

Do not describe only individual functions.

Derive the behavior-driving dimensions from requirement + current source + patch.

Typical dimensions:

- endpoint / operation
- selector / request mode
- parameter present/absent/value class
- body field combinations
- storage/model/type
- feature/config flag
- upgrade/legacy state
- external response state

For small finite dimensions, enumerate all meaningful combinations.
For large dimensions, use equivalence classes + boundaries + pairwise/risk-based combinations.

Required table:

| Case ID | Entry Point / Endpoint | Preconditions | Request / Input Combination | Baseline Behavior | Patched Behavior | Expected Behavior | Compatibility | Evidence |
|---|---|---|---|---|---|---|---|---|

`Expected Behavior` must be evidence-backed.
If the requirement does not define it and source cannot establish it, write `EXPECTED_BEHAVIOR_UNRESOLVED` and name the missing evidence. Do not invent an oracle.

# 8. Test Viewpoint Derivation

For each impacted surface derive only applicable viewpoints.

Candidate viewpoints:

### Contract / API
- existing request backward compatibility
- new parameter/field positive cases
- omitted/null/empty/default
- valid combinations
- invalid combinations
- boundary/format/range
- response field presence/absence/nullability
- HTTP status and error code
- version compatibility

### Runtime / business rule
- branch true/false
- model/type/state variants
- old/new representation
- fallback/error paths

### Integration
- exact external command/options/request
- parser mapping
- missing/extra downstream fields
- downstream error mapping

### Data/state
- persistence/read-back
- key lookup/equality
- cache behavior
- migration/legacy data

### Non-functional regression
- no additional expensive downstream mode for unchanged requests
- no additional call count where performance-sensitive
- idempotency/concurrency only if the changed path involves them

Do NOT create generic security/performance/concurrency tests when there is no source-backed impact.

# 9. Test-Level Selection

Map each test to the lowest level that can prove the behavior, while retaining end-to-end coverage for externally observable contracts.

Use:

```text
UNIT
COMPONENT
API_CONTRACT
INTEGRATION
END_TO_END
REGRESSION
```

Do not propose only unit tests for an API-visible change.

# 10. Required Test Matrix

| Test ID | Level | Endpoint / Entry Point | Viewpoint | Preconditions | Input / Request | Expected Downstream Interaction | Expected Response / State | Regression Purpose | Evidence |
|---|---|---|---|---|---|---|---|---|---|

Every HIGH/CRITICAL impact must map to at least one concrete test.
Every changed API contract rule must map to at least one API_CONTRACT or higher-level test unless technically impossible; explain exceptions.

# 11. Mandatory Impact Inventories

## 11.1 Changed Code Surface

| File | Class/Symbol | Change | Runtime Role |
|---|---|---|---|

## 11.2 Runtime Impact

| Class/Component | Method/Behavior | Why Impacted | Direct/Indirect | Patch Touches It? | Evidence |
|---|---|---|---|---|---|

## 11.3 API Contract Impact

| API | Method + Path | Request Contract Impact | Response Contract Impact | Error/Status Impact | Compatibility Risk | Evidence |
|---|---|---|---|---|---|---|

If none, include one row stating `NO_DIRECT_REST_API_IMPACT` with evidence.

## 11.4 External Contract Impact

| Boundary | Operation | Input Before/After | Output Before/After | Failure Impact | Evidence |
|---|---|---|---|---|---|

# 12. Risk Table

| Risk ID | Surface | Scenario | Severity | Likelihood | Evidence | Required Verification |
|---|---|---|---|---|---|---|

Severity and likelihood must be justified from the actual behavior; do not assign decorative ratings.

# 13. Coverage Gate

Before finalizing, answer explicitly:

```text
[ ] Changed functions traced to callers and callees
[ ] API reachability determined
[ ] Affected endpoint(s) identified or NO_DIRECT_REST_API_IMPACT proven
[ ] Request parameters/body/header impact checked
[ ] Response/status/error contract checked
[ ] External integrations checked
[ ] Data/persistence/config/cache impact checked
[ ] Backward compatibility checked
[ ] Performance-sensitive downstream behavior checked
[ ] Behavior matrix created
[ ] Test viewpoints derived from actual impact
[ ] Expected behavior has an evidence-backed oracle
[ ] Every HIGH/CRITICAL impact maps to a test
```

The review is incomplete if any applicable item is omitted without explanation.

# 14. Output

Default output:

```text
docs/reverse-engineering/reviews/<patch>-impact-review.md
```

Required sections:

1. Executive Conclusion
2. Requirement / Intended Behavior
3. Patch Intent and Implementation Summary
4. Changed Code Surface
5. Exposure and Runtime Flow
6. REST / HTTP API Contract Impact
7. External Integration Contract Impact
8. Data / State / Configuration Impact
9. Before-vs-After Behavior Matrix
10. Compatibility and Regression Risks
11. Missing / Insufficient Patch Coverage
12. Test Viewpoints
13. Test Matrix with Expected Behavior
14. Evidence Index
15. Coverage Gate Result

# 15. Final Decision

Use project-appropriate decision values, for example:

```text
PATCH_SUFFICIENT
PATCH_PARTIALLY_SUFFICIENT
PATCH_INSUFFICIENT
```

The decision must be based on requirement coverage + observable contract impact + regression evidence, not on changed-file count.
