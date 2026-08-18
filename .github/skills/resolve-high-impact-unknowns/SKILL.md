---
name: resolve-high-impact-unknowns
description: Actively close HIGH/CRITICAL reverse-engineering unknowns by dispatching targeted source tracing, requiring search-exhaustion evidence before external blocking, and preventing premature baseline-readiness claims.
license: MIT
---

# Resolve High-Impact Unknowns

## Mission

Do not merely list high-impact unknowns.
Close them where the repository can answer them.

## Inputs

Read:

```text
00_open_questions.md
00_workflow_state.md
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
Communication config unknown.
```

Better:

```text
Which source/key/default/override chain determines runtime communication mode used by Factory X for operation family Y?
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
- call sites
- related constants/enums

### 4. Record Search Coverage

Before unresolved closure, record what was actually searched.

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
- code-side boundary/injection point identified when possible
- exact missing external artifact/value/evidence named

### 6. Promote If Appropriate

Resolved architectural facts still pass `/claim-verification-and-promotion` before canonical promotion.

## Required Closure Matrix

| Q-ID | Impact | Question | Investigation Performed | Source Result | Closure State | Evidence/Artifact | Remaining External Evidence |
|---|---|---|---|---|---|---|---|

## Loop

Continue until:

```text
HIGH/CRITICAL SOURCE_SEARCH_PENDING = 0
```

or context/tool limits require `PARTIAL_RESUMABLE`.

If limits are hit, persist exact next Q-ID, search anchor, and skill to run.

## Output

Create/update:

```text
docs/reverse-engineering/09_high_impact_unknown_closure.md
```

Also update:

```text
00_open_questions.md
00_workflow_state.md
00_investigation_coverage.md
00_evidence_ledger.md
```

Do not print the full report to console.
