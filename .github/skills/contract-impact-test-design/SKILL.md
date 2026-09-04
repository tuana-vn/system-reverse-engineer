---
name: contract-impact-test-design
description: Convert a source-backed patch or requirement impact analysis into contract-level test viewpoints, provenance-aware expected behavior, and spreadsheet-style Check ID matrices. Use when external operations, request/input dimensions, downstream data availability, field/data mapping, validation combinations, and observable results must be tested after a change.
---

# Contract Impact Test Design — 4.0

## Purpose

Turn verified impact surfaces into an executable QA-oriented test design.

This skill exists because:

```text
FUNCTION IMPACT != API CONTRACT IMPACT != TEST DESIGN
```

A list of impacted methods is not a test plan.
A list of impacted endpoints is not a test matrix.

The skill must connect:

```text
change / requirement
→ external operation
→ request contract
→ runtime selection
→ integration / state behavior
→ observable result
→ test viewpoint
→ Check ID
```

## Inputs

Use the strongest available evidence in this order:

1. explicit requirement/specification
2. current source
3. promoted verified reverse-engineering baseline
4. source-backed patch impact report
5. patch/diff as candidate future behavior
6. existing tests as behavioral evidence, not unquestioned truth

Do not invent missing contracts or expected results.


## Step 0 — Canonical Requirement / Scope Matrix

When an explicit requirement/specification exists, normalize it before deriving tests.

Create:

| Rule | External Operation / Surface | Applies? | Condition | Expected Observable Behavior |
|---|---|---:|---|---|

Rules:

- Evaluate each row independently.
- Do not transfer conditions from one endpoint/operation/surface to another.
- A condition applies only where the requirement explicitly assigns it.
- Preserve explicit exclusions and non-applicable surfaces.
- If scope cannot be proven, mark it `SCOPE_UNRESOLVED`.
- Use this matrix as the authoritative scope for later test derivation.

This prevents a condition from one operation from leaking into another operation's test oracle.

## Step 1 — Impacted External Operation Inventory

For every material impact, identify all externally reachable operations that can observe it.

Possible entry types include:

- REST API
- CLI
- scheduled job
- message/event consumer
- file/config import
- other source-confirmed public interfaces

For REST, record:

| API ID | Method | Exact Path | API Version | Handler | Why Impacted | Evidence |
|---|---|---|---|---|---|---|

If no external operation is reachable, classify and prove:

```text
NO_DIRECT_EXTERNAL_INTERFACE_IMPACT
```

Do not stop at class/method names.

## Step 2 — Request Contract Inventory

For every impacted REST operation enumerate the request dimensions needed to reach and distinguish affected behavior.

### GET / DELETE

Inspect:

- path params
- query params
- headers
- required/optional
- omitted behavior
- empty/null where representable
- defaults
- enum/range/format
- selector rules
- parameter combinations

### POST / PUT / PATCH

Inspect all of the above plus:

- content type
- body DTO/model
- body required/optional
- top-level fields
- relevant nested fields
- arrays/collections where relevant
- null/empty/default
- enum/range/format
- cross-field combinations

Create:

| API ID | Input Location | Field/Parameter | Type | Required? | Valid Classes | Invalid/Boundary Classes | Default/Omitted Behavior | Combination Rules | Impact Relevance | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|

Do not restrict inventory to newly added fields. Include existing selectors/fields needed to reach the impacted runtime path.


## Step 2A — Input / Parameter Semantics Gate

When the interface accepts named parameters or structured inputs, keep these classes distinct:

- valid supported parameter/input
- unsupported parameter/input name
- wrong-case parameter/input name
- invalid value of a supported parameter/input
- invalid combination of supported parameters/inputs
- omitted / null / empty / default, when applicable

Do not conflate them.

If the specification defines case sensitivity, unsupported-input behavior, defaults,
or ignore rules, preserve those semantics exactly.

Do not infer an error oracle merely because an input is unknown or malformed.
The expected result must come from requirement/specification or verified source behavior.

## Step 3 — Preconditions and Environment Dimensions

Identify source/requirement-backed conditions such as:

- storage/product/model
- upgraded/non-upgraded state
- feature flags
- authentication/authorization role
- existing resource state
- real/virtual classification
- integration availability
- persisted/configured state

Create equivalence classes rather than arbitrary examples.

## Step 4 — Observable Behavior Inventory

For every impacted path identify applicable expected observables:

### API

- HTTP status
- domain/product error code
- response field/value
- field presence/absence
- null/default behavior
- headers if relevant

### Integration / command

- command type
- command parameters
- downstream identifier/serial
- call/no-call
- call ordering when relevant
- response parser/normalization behavior

### Data / state

- persisted value
- config output
- cache/map identity
- classification outcome
- created/updated/deleted state

If the expected oracle cannot be proven, use:

```text
EXPECTED_BEHAVIOR_UNRESOLVED
```

and identify exactly what is missing.


## Step 4A — Field / Data Provenance Inventory

For every response/output/state value affected by the change, prove the value lifecycle
before using it as a test oracle.

Create:

| Operation | Field/Data | Request/Trigger Condition | Downstream Retrieval | Source Field/Data | Transform/Normalize | Mapping/Storage | Serialization/Output | Final Observable Behavior | Evidence |
|---|---|---|---|---|---|---|---|---|---|

Determine independently:

1. under what condition the source/downstream data is obtained
2. which command/query/call/branch makes it available
3. where it is parsed or decoded
4. where it is transformed or normalized
5. where it is mapped/stored
6. what happens when it is absent or not retrieved
7. how it is serialized/emitted/consumed
8. what externally observable result follows

Important:

- Conditional output behavior may be implemented indirectly by conditional retrieval.
- Do not require an explicit serializer/output-layer condition when upstream retrieval
  and mapping already guarantee the required observable behavior.
- Current implementation shape is not itself the expected test oracle.
- If provenance cannot be proven, use `EXPECTED_BEHAVIOR_UNRESOLVED`.

## Step 5 — Derive Test Viewpoints

Derive viewpoints from contract and impact dimensions, not methods.

Applicable viewpoints may include:

1. existing-request backward compatibility
2. new behavior positive path
3. feature/condition absent path
4. required parameter/body field omitted
5. optional parameter/body field omitted
6. null/empty/default
7. enum/range/format boundary
8. valid selector combinations
9. invalid selector combinations
10. cross-field combinations
11. upgraded/non-upgraded or version/model variants
12. legacy/unaffected regression
13. correct downstream command/argument
14. downstream call must not occur on validation failure
15. downstream response normalization
16. response field/value/presence
17. HTTP status/domain error mapping
18. persisted/configured/state effect
19. real/virtual or equivalent classification outcome
20. integration error handling when source defines it

Do not create a viewpoint when source proves it irrelevant.


## Step 5A — Test Oracle Chain

For every Check ID involving changed output/data, the expected result must be traceable as:

```text
requirement / verified expected rule
→ trigger / request condition
→ expected source/downstream data availability
→ expected transform/mapping/state
→ expected serialization/output
→ externally observable result
```

Do not derive expected behavior solely from current implementation.
Do not create a serializer-level expectation when the observable condition is enforced earlier
in the data flow.

If any material link is unproven, mark the case:

`BLOCKED_MISSING_ORACLE`

and name the missing evidence.

## Step 6 — Combination Strategy

Do not blindly generate the Cartesian product.

Use, in order:

1. explicit requirement combinations
2. source validation branches
3. equivalence partitioning
4. boundary-value analysis
5. decision-table combinations
6. pairwise/risk-based combinations for independent dimensions
7. regression cases for unchanged behavior

HIGH/CRITICAL impacts require direct coverage of each material branch.

## Step 7 — Assign Check IDs

Assign stable IDs:

```text
001
002
003
...
```

Each Check ID must represent one coherent scenario with:

- precondition
- operation
- concrete request setup
- expected runtime/integration behavior
- expected API/domain result
- expected response/state

Do not combine materially different request variants under one Check ID.

## Step 8 — Spreadsheet-Style Cross Matrix

Generate a cross matrix where columns are Check IDs and rows are conditions/confirmation items.

Required row groups when applicable:

```text
Precondition
API
  Method + endpoint
  Path parameters
  Query parameters
  Headers
  Body / payload
Command / downstream interaction
Expected results
  HTTP status
  Domain error
  Response fields/state
```

Use `O` to mark a condition applicable to a Check ID.

Example shape:

```text
Check conditions / confirmation items | 001 | 002 | 003
Precondition
  upgraded storage                    |  O  |  O  |
  non-upgraded storage                |     |     | O
API
  GET /4.0/items                       |  O  |  O  |
    query: detail=true                |  O  |     |
    query: detail absent              |     |  O  |
  POST /4.0/items                      |     |     | O
    body.mode=valid                   |     |     | O
Expected results
  HTTP 200                            |  O  |  O  | O
```

This matrix is mandatory when two or more scenarios exist.

## Step 9 — Detailed Test Case Table

Mandatory table:

| Check ID | Level | Precondition | Method | Endpoint / Entry Point | Path Params | Query Params | Headers | Body/Payload | Expected Downstream / Runtime | Expected Data Provenance / State | Expected HTTP Status | Expected Domain Error | Expected Response / State | Regression Purpose | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Levels:

```text
UNIT
COMPONENT
API_CONTRACT
INTEGRATION
END_TO_END
REGRESSION
```

Rules:

- API-visible impact cannot be covered only by UNIT tests.
- GET rows must include concrete query/path/header setup when relevant.
- POST/PUT/PATCH rows must include concrete payload setup when relevant.
- Validation cases must specify expected downstream call/no-call where provable.
- Expected values must be evidence-backed.

## Step 10 — CSV Export

When requested by the calling prompt, create a spreadsheet-friendly CSV with one row per Check ID.

Minimum columns:

```text
CheckID
Level
Precondition
HttpMethod
Endpoint
PathParams
QueryParams
Headers
BodyPayload
ExpectedRuntimeBehavior
ExpectedDataProvenanceOrState
ExpectedHttpStatus
ExpectedDomainError
ExpectedResponseOrState
RegressionPurpose
Evidence
```

Quote values correctly when they contain commas/newlines.

## Traceability Gate

Every material requirement/impact must map to at least one Check ID or an explicit justified no-test classification.

Create:

| Requirement / Impact | API / Entry Point | Contract Dimension | Check IDs | Coverage Status | Evidence |
|---|---|---|---|---|---|

Coverage statuses:

```text
COVERED
PARTIALLY_COVERED
NOT_COVERED
NOT_APPLICABLE
BLOCKED_MISSING_ORACLE
```

## Completion Gate

The skill MUST NOT complete until all applicable items pass:

```text
[ ] canonical requirement/scope matrix created when an explicit requirement exists
[ ] external operations identified or non-exposure proven
[ ] exact REST method/path captured
[ ] GET path/query/header parameters enumerated
[ ] POST/PUT/PATCH body fields enumerated
[ ] validation, case-sensitivity, unsupported-input, and combination semantics considered
[ ] precondition/environment dimensions considered
[ ] field/data provenance proven for changed output/state or unresolved explicitly
[ ] expected downstream behavior defined or unresolved explicitly
[ ] HTTP/domain/response/state oracle is tied to a requirement + provenance chain or unresolved explicitly
[ ] no condition was transferred from another endpoint/operation without evidence
[ ] Check IDs assigned to concrete scenarios
[ ] cross matrix generated
[ ] detailed testcase table generated
[ ] API-visible impacts have API_CONTRACT-or-higher coverage where feasible
[ ] traceability from impact/requirement to Check IDs exists
```

If a completion item cannot pass because evidence is missing, report the blocker rather than guessing.

## Anti-Patterns

Do NOT produce only:

```text
- changed classes/functions
- impacted methods
- endpoint names without request dimensions
- generic "positive/negative" test bullets
- unit-test method suggestions without API contract cases
- expected behavior inferred from intuition
```

The target artifact is a **contract-level test design**, not a code coverage list.
