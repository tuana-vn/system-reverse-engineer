---
name: resolve-high-impact-unknowns
description: Actively close HIGH/CRITICAL reverse-engineering unknowns by dispatching targeted source tracing, requiring search-exhaustion evidence before external blocking, and preventing premature baseline-readiness claims.
---

# Resolve High-Impact Unknowns — 4.0

## Mission

Do not merely list high-impact unknowns.
Close them where the repository can answer them.

## Inputs

Read:

```text
00_open_questions.md
workflow_state.yaml  # runner-owned authoritative state for the active workflow
00_investigation_coverage.md
00_current_understanding.md
00_evidence_ledger.md
```

Load only relevant detailed artifacts per question.

## Prioritization

Process:

```text
CRITICAL first
then HIGH
```

Within equal impact, prefer questions that block multiple downstream claims or tasks.

## For Each Question

### 1. Restate the Missing Fact

Make it specific and falsifiable.

Bad:

```text
Checkout timeout source is unknown.
```

Better:

```text
Which configuration source, key, default, and override chain determines the checkout timeout used by the Python order worker?
```

Also make provenance/exposure questions falsifiable.

Examples:

```text
Under which checkout request conditions is the promotion code retrieved, normalized, and returned in the order response?
```

```text
Which REST endpoints, message consumers, or scheduled jobs can reach the C++ pricing-engine boundary after enumerating every source-visible invocation site?
```

### 2. Determine Investigation Domain

Dispatch one or more skills:

```text
configuration source / mode
→ /configuration-source-trace

runtime implementation / DI / factory binding
→ /runtime-binding-verification

persistence / DB schema / DAO
→ /persistence-schema-reverse-engineering

end-to-end operation behavior
→ /runtime-flow-analysis

integration routing
→ /integration-selection-analysis

field/data provenance
→ /runtime-flow-analysis plus targeted source trace through retrieval → mapping → output

external exposure from a known downstream boundary
→ boundary → exposure closure using caller/reference tracing

other
→ targeted source trace using system-reverse-engineer rules
```

### 3. Search From Multiple Anchors

Do not rely on the original search that produced UNKNOWN.

Use alternate anchors:

- consumer backward
- source/config forward
- symbol references
- implementations
- startup/bootstrap
- tests
- migrations/scripts
- all direct call/construction sites
- caller fan-out from impacted downstream boundaries
- serializers/mappers/parsers
- related constants/enums

### 4. Record Search Coverage

Before unresolved closure, record what was actually searched.


### 4A. Provenance / Exposure Closure Requirements

When the unknown concerns externally meaningful data, do not resolve it until the material chain is closed:

```text
trigger
→ source/downstream retrieval
→ source data
→ parse/transform
→ mapping/state
→ serialization/output
→ observable result
```

When the unknown concerns external reachability of a known downstream boundary:

```text
boundary
← ALL direct invocation/construction sites
← ALL caller chains
← external entry points / proven internal roots
```

Do not resolve reachability based on one representative endpoint.

If one direct invocation site remains unresolved, the question remains:

`SOURCE_SEARCH_PENDING`

or `SOURCE_SEARCH_IN_PROGRESS`.

### 5. Resolve

Use one:

```text
RESOLVED_VERIFIED
RESOLVED_REJECTED
NOT_APPLICABLE
EXTERNALLY_BLOCKED
SOURCE_SEARCH_PENDING
```

`EXTERNALLY_BLOCKED` requires:

- repository search sufficiently exhausted
- alternate anchors used
- provenance chain traced as far as source allows when data/output-related
- all source-visible invocation sites classified when reachability-related
- code-side boundary/injection point identified when possible
- exact missing external artifact/value/evidence named

### 6. Promote If Appropriate

Resolved architectural facts still pass `/claim-verification-and-promotion` before canonical promotion.

## Required Closure Matrix

| Q-ID | Impact | Question | Investigation Performed | Provenance / Exposure Closure | Source Result | Closure State | Evidence/Artifact | Remaining External Evidence |
|---|---|---|---|---|---|---|---|---|

## Loop

Continue until:

```text
HIGH/CRITICAL SOURCE_SEARCH_PENDING = 0
```

or context/tool limits require `PARTIAL_RESUMABLE`.

If limits are hit, persist exact next Q-ID, unresolved provenance/exposure link,
search anchor, and skill to run.

## Output

Create/update:

```text
docs/reverse-engineering/09_high_impact_unknown_closure.md
```

Also update:

```text
00_open_questions.md
workflow_state.yaml  # runner-owned authoritative state for the active workflow
00_investigation_coverage.md
00_evidence_ledger.md
```

Do not print the full report to console.


## 4.0 Source-Fact Boundary

`RESOLVED_VERIFIED` applies to the source question, not to downstream design recommendations.

```text
NO CURRENT MECHANISM FOUND
!=
SPECIFIC FUTURE MECHANISM VERIFIED
```

If implementation guidance is useful, label it `PROPOSED` and do not promote it into the evidence
ledger as source truth.


## 4.0 Run-Scoped State Isolation

When this skill is invoked by a workflow whose `state_path` is under
`docs/reverse-engineering/runs/<run_id>/`, do not create or update ``workflow_state.md` or any second state file. The runner owns the single authoritative
workflow-declared YAML state file.
