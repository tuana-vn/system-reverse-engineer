---
name: patch-impact-review
description: Review a patch or Git diff against the evidence-backed current-system baseline, trace changed behavior through observable surfaces, runtime dependencies, integrations, and field/data provenance, identify compatibility/regression risks, and derive evidence-backed verification. Require scope isolation, provenance, and completion gates before declaring impact or sufficiency.
license: MIT
---

# Patch Impact Review 4.0 — Contract + Runtime + Exposure Closure + Provenance + Test Impact

## Purpose

A patch impact review is NOT a changed-function inventory.

```text
PATCHED CODE
→ changed runtime rule
→ affected observable surface
→ affected input/output contract
→ affected field/data provenance
→ affected integration/data/state behavior
→ compatibility/regression risk
→ required verification
```

A changed method is only the starting point.

## 0. Baseline Safety

- CURRENT SOURCE = baseline behavior authority.
- PATCH/DIFF = candidate changed behavior.
- REQUIREMENT/SPEC = intended behavior.
- Promoted reverse-engineering memory is supporting evidence, not a substitute for current source.
- If requirement, source, and patch disagree, show the disagreement explicitly.
- Never update canonical baseline memory from an unmerged patch.
- Do not reuse a previous review conclusion as evidence.

## 1. Inputs

Use all applicable inputs:

- patch / Git diff
- current source
- promoted reverse-engineering baseline
- requirement / issue / customer clarification
- API/interface specification
- tests and fixtures
- integration protocol definitions
- configuration and persistence schema

Record missing evidence instead of guessing.

## 2. Normalize Intended Behavior

Create atomic rules `R-001`, `R-002`, ...

For each rule capture:

- observable surface / endpoint / operation
- trigger and preconditions
- supported inputs/parameters
- expected behavior and output/state
- failure/exception behavior
- compatibility requirement
- explicit exclusions / non-applicable surfaces
- ambiguity

Do not invent acceptance criteria.

### 2.1 Canonical Requirement / Scope Matrix

When a requirement exists, create:

| Rule | Surface / Operation | Applies? | Condition | Expected Observable Behavior |
|---|---|---:|---|---|

Rules:

- Evaluate each row independently.
- Do not transfer conditions between endpoints/surfaces/operations.
- A condition applies only where explicitly assigned.
- If scope is ambiguous, mark `UNKNOWN`.
- Use this matrix as authoritative scope for impact and sufficiency judgments.

## 3. Reconstruct the Change at Three Levels

### 3.1 Business Purpose
Why the change is needed.

### 3.2 Observable Functional Behavior
What an external caller, operator, job, integration, or persisted state can observe before vs after.

For a bug fix:

```text
Observed Problem
→ PATCH-IMPLIED ROOT CAUSE
→ Changed Rule
→ Corrected Observable Behavior
```

Label patch-implied root cause unless source-verified.

### 3.3 Technical Implementation

Identify:

- changed files/symbols
- changed conditions/branches
- transformations
- integration calls
- .ai-engineering/state-templates/configuration changes

Do not infer correctness from implementation shape.

## 4. Mandatory Impact-Surface Discovery

For every semantically changed behavior, trace both directions.

### Upstream / Exposure Trace

```text
changed symbol
← callers
← service/facade/handler
← controller/resource/router/entry point
← endpoint/event/job/CLI/GUI/RPC surface
```

### Downstream / Effect Trace

```text
changed symbol
→ callees/utilities
→ integration/client/DB/message/config/file
→ parser/transformation
→ response/.ai-engineering/state-templates/side effect
```

Stop only at:

```text
EXTERNALLY_EXPOSED
INTERNAL_ONLY
BACKGROUND_OR_SCHEDULED
EXTERNAL_INTEGRATION_ONLY
SOURCE_NOT_RESOLVED
```

Do not stop at the first caller or callee.


## 4A. Boundary → Exposure Closure Gate

The upstream trace from a changed symbol is not sufficient when impact is discovered
at a downstream integration/runtime boundary.

Whenever an impacted boundary is confirmed, such as:

- native executable / external process invocation
- RPC/SDK operation
- DB query
- message producer
- file/config writer
- persistence operation
- downstream service call

treat that boundary as a new reverse-trace seed.

### Required algorithm

1. Enumerate ALL source-visible direct invocation/construction sites of the boundary.
2. For EACH site, trace callers upward independently.
3. Continue until an external entry point or proven non-external root is reached.
4. If caller chains fan out, follow every material branch.
5. If caller chains converge, preserve the distinct external entry points.
6. Do not stop after finding one representative endpoint.

Required trace:

```text
impacted boundary
← invocation/construction site
← business/service caller
← handler/controller/resource/router
← exact external operation
```

### Boundary terminology

Do not confuse a downstream CLI integration with a product CLI entry point:

- `DOWNSTREAM_PROCESS_INTEGRATION`: the application invokes an external executable or native process.
- `PRODUCT_COMMAND_ENTRY_POINT`: a user/operator enters the application through its own command interface.

### Exposure Closure Matrix

| Boundary ID | Impacted Boundary | Invocation Site | Caller Chain | External Entry Type | Method | Exact Path / Operation | Classification | Evidence |
|---|---|---|---|---|---|---|---|---|

Classifications:

```text
REST_REACHABLE
PRODUCT_COMMAND_REACHABLE
JOB_REACHABLE
EVENT_REACHABLE
GUI_REACHABLE
RPC_REACHABLE
INTERNAL_ONLY
SOURCE_NOT_RESOLVED
```

### Closure rule

An impacted boundary is not exposure-complete until every source-visible direct
invocation/construction site is classified.

`NO_DIRECT_REST_API_IMPACT` or any equivalent no-impact claim is forbidden while
a direct invocation site remains unresolved.

This gate is mandatory even when a broad external-interface inventory was already performed.


## 5. Input / Parameter Semantics Gate

When changed behavior is input-driven, distinguish:

- valid supported input/parameter
- unsupported input/parameter name
- wrong-case input/parameter name
- invalid value of a supported input/parameter
- invalid combination of supported inputs/parameters
- omitted / null / empty / default

Do not conflate these categories.

Preserve exact specification rules for case sensitivity, defaults, and unsupported inputs.
Do not infer error behavior from naming alone.

## 6. External Contract Impact

Inspect all reachable external boundaries.

### REST / HTTP
Check:

- method/path/version
- path/query/header/body fields
- required/optional/null/default
- allowed values/format/range
- parameter-combination rules
- case sensitivity / unsupported-parameter behavior
- status codes
- response fields/type/format
- conditional field presence
- null vs omitted
- error mapping
- filtering/pagination/ordering
- backward compatibility

If no REST impact, state `NO_DIRECT_REST_API_IMPACT` and prove it with the exposure trace.

### Non-REST
Inspect applicable:

- CLI
- GUI
- RPC
- external SDK/API
- DB
- event/message
- file/configuration
- cache
- batch/scheduler
- authn/authz
- logs/audit/metrics when behaviorally significant

For each boundary trace:

```text
input → transformation → output/side effect → failure behavior
```

## 7. Field / Data Provenance Gate

For every changed, introduced, filtered, normalized, persisted, or conditionally exposed value, prove its lifecycle before declaring impact or no-impact.

| Surface | Field/Data | Trigger/Condition | Source Retrieval | Source Field/Data | Transform/Normalize | Mapping/Storage | Serialization/Output | Final Observable Behavior | Evidence |
|---|---|---|---|---|---|---|---|---|---|

Determine:

1. When is source data obtained?
2. Which command/query/call/branch makes it available?
3. Where is it parsed?
4. Where is it transformed/normalized?
5. Where is it mapped/stored?
6. What happens when it is absent or not retrieved?
7. How is it serialized/emitted/consumed externally?
8. What observable behavior results?

Important:

- Conditional behavior may be implemented indirectly by conditional retrieval.
- Do not require an explicit output-layer condition if earlier data-flow decisions already produce correct behavior.
- A changed output field does not imply the serializer is the root of impact.
- Extra internal retrieval is not automatically a contract violation.
- Report evidenced performance or side-effect risk separately.

This gate applies to REST responses, CLI output, persisted state, messages, configuration, identifiers, and other externally meaningful values.

## 8. Data and State Impact

Trace changed values through:

- parsing
- validation
- normalization/conversion
- persistence
- equality/comparison
- cache/map keys
- serialization/deserialization
- response mapping
- command construction
- configuration generation
- logging/display

For identifier-like values also check:

- prefix/range/length assumptions
- numeric/string conversion
- arithmetic
- truncation/padding
- uniqueness/collision
- backward-compatible lookup

## 9. Compatibility and Regression Impact

Evaluate separately:

- functional compatibility
- API compatibility
- integration compatibility
- data compatibility
- performance compatibility
- security compatibility when intersected

For performance, check:

- external call count
- data volume
- expensive query/command modes
- loops/retries
- cache changes
- DB query shape

Do not misclassify secondary performance/design concerns as requirement violations unless the requirement covers them.

## 10. Mandatory Before-vs-After Behavior Matrix

| Case ID | Entry Point / Endpoint | Preconditions | Request / Input Combination | Baseline Behavior | Patched Behavior | Expected Behavior | Compatibility | Evidence |
|---|---|---|---|---|---|---|---|---|

Derive dimensions from requirement + current source + patch.

If expected behavior cannot be established, write:

`EXPECTED_BEHAVIOR_UNRESOLVED`

and name the missing evidence.

## 11. Impact Claim Completion Gate

Do not declare:

- `IMPACTED`
- `NOT_IMPACTED`
- `PATCH_SUFFICIENT`
- `PATCH_PARTIALLY_SUFFICIENT`
- `PATCH_INSUFFICIENT`

until the applicable chain is proven.

For externally observable changes:

```text
changed code
→ runtime path
→ impacted downstream boundary (when applicable)
→ ALL invocation/construction sites
→ ALL reachable external surfaces
→ input condition
→ downstream/data provenance
→ mapping/.ai-engineering/state-templates/output
→ externally observable result
```

For `NO_DIRECT_*_IMPACT`, prove that the exposure trace terminates before an external surface.

For changed response/output/data fields, the Field / Data Provenance Gate is mandatory.

If a required link cannot be proven:

- use `SOURCE_NOT_RESOLVED`
- use `EXPECTED_BEHAVIOR_UNRESOLVED` where applicable
- do not fill the gap with assumptions

## 12. Adversarial Reverification

Before finalizing every HIGH/CRITICAL impact, no-impact claim, or insufficiency claim:

- search alternate callers
- search alternate downstream paths
- search earlier conditional retrieval/mapping
- search serializers/mappers/configuration that contradict the initial finding
- verify conditions were not borrowed from another surface
- inspect tests that could prove or disprove the finding

A user correction is not evidence.

If challenged:

- reopen the finding
- re-trace source
- search counterevidence
- revise only when source evidence supports revision

Do not change a finding merely to agree with the user.

## 13. Test Viewpoint Derivation

Derive only applicable viewpoints.

### Contract/API
- backward compatibility
- new field/parameter positive cases
- omitted/null/empty/default
- valid/invalid combinations
- unsupported/wrong-case names when applicable
- boundary/format/range
- response presence/absence/nullability
- HTTP/error behavior

### Runtime/business rule
- branch true/false
- model/type/state variants
- old/new representation
- fallback/error paths

### Integration
- exact downstream command/options/request
- parser mapping
- missing/extra downstream fields
- downstream error mapping

### Data/state
- persistence/read-back
- key/equality
- cache
- migration/legacy data

### Non-functional
- no extra expensive downstream mode for unchanged requests
- no extra call count where performance-sensitive
- idempotency/concurrency only when impacted

Do not create generic tests without source-backed impact.

## 14. Test-Level Selection

Use:

```text
UNIT
COMPONENT
API_CONTRACT
INTEGRATION
END_TO_END
REGRESSION
```

Use the lowest level that proves the rule, while retaining end-to-end coverage for external contracts.

## 15. Required Test Matrix

| Test ID | Level | Endpoint / Entry Point | Viewpoint | Preconditions | Input / Request | Expected Downstream Interaction | Expected Data Provenance / State | Expected Response / State | Regression Purpose | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|

Every HIGH/CRITICAL impact must map to at least one concrete test.
Every changed external contract rule must map to API_CONTRACT or higher unless technically impossible.

## 16. Mandatory Inventories

### Changed Code Surface

| File | Class/Symbol | Change | Runtime Role |
|---|---|---|---|

### Runtime Impact

| Class/Component | Method/Behavior | Why Impacted | Direct/Indirect | Patch Touches It? | Evidence |
|---|---|---|---|---|---|

### Boundary → Exposure Closure

| Boundary | Invocation Site | Caller Chain | External Entry Type | Method | Exact Path / Operation | Classification | Evidence |
|---|---|---|---|---|---|---|---|

### API Contract Impact

| API | Method + Path | Request Contract Impact | Response Contract Impact | Error/Status Impact | Compatibility Risk | Evidence |
|---|---|---|---|---|---|---|

### External Contract Impact

| Boundary | Operation | Input Before/After | Output Before/After | Failure Impact | Evidence |
|---|---|---|---|---|---|

### Field / Data Provenance Impact

| Surface | Field/Data | Before Provenance | After Provenance | Observable Change | Risk | Evidence |
|---|---|---|---|---|---|---|

## 17. Risk Table

| Risk ID | Surface | Scenario | Severity | Likelihood | Evidence | Required Verification |
|---|---|---|---|---|---|---|

Severity and likelihood must be justified by actual behavior.

## 18. Coverage Gate

```text
[ ] Requirement/scope matrix created when requirement exists
[ ] Changed functions traced to callers and callees
[ ] External reachability determined
[ ] Every impacted downstream boundary has all direct invocation/construction sites enumerated
[ ] Every invocation site is reverse-traced to an external or proven internal root
[ ] Shared runtime/integration paths enumerate all distinct external entry points
[ ] Affected endpoints/surfaces identified or no-impact proven
[ ] Input/parameter semantics checked
[ ] Request/body/header impact checked
[ ] Response/status/error contract checked
[ ] Field/data provenance proven for changed output/data
[ ] External integrations checked
[ ] Data/persistence/config/cache impact checked
[ ] Backward compatibility checked
[ ] Performance-sensitive downstream behavior checked
[ ] Before-vs-after behavior matrix created
[ ] Expected behavior has an evidence-backed oracle
[ ] HIGH/CRITICAL claims adversarially reverified
[ ] Every HIGH/CRITICAL impact maps to a test
[ ] No-impact claims have a terminating source trace
```

The review is incomplete if any applicable item is omitted without explanation.

## 19. Output

Default:

`docs/reverse-engineering/reviews/<patch>-impact-review.md`

Required sections:

1. Executive Conclusion
2. Requirement / Intended Behavior
3. Canonical Requirement / Scope Matrix
4. Patch Intent and Implementation Summary
5. Changed Code Surface
6. Exposure and Runtime Flow
7. REST / HTTP API Contract Impact
8. External Integration Contract Impact
9. Field / Data Provenance Impact
10. Data / State / Configuration Impact
11. Before-vs-After Behavior Matrix
12. Compatibility and Regression Risks
13. Missing / Insufficient Patch Coverage
14. Test Viewpoints
15. Test Matrix with Expected Behavior
16. Evidence Index
17. Coverage Gate Result

## 20. Final Decision

Use:

```text
PATCH_SUFFICIENT
PATCH_PARTIALLY_SUFFICIENT
PATCH_INSUFFICIENT
CANNOT_VERIFY
```

Base the decision on:

```text
requirement scope
+ observable contract impact
+ complete runtime/data provenance
+ compatibility/regression evidence
```

not changed-file count or implementation shape.
