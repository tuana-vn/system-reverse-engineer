---
name: architecture-drift-detection
description: Compare current source code against the stored evidence-backed reverse-engineering baseline to identify stale architectural knowledge, undocumented routing changes, new integrations, removed behavior, or prior baseline errors.
license: MIT
---

# Architecture Drift Detection

## Principle

The source is the primary truth.

The stored reverse-engineering baseline may become stale.

## Compare

Check high-value baseline claims against current source:

- inbound interfaces
- client implementations
- selectors/factories
- configuration
- target/model/mode branches
- integrations
- protocol boundaries
- retry/fallback
- error mappings

## Drift Matrix

| Baseline Claim | Current Source | Status | Severity | Evidence | Baseline Update Needed |
|---|---|---|---|---|---|

Status:

- NO DRIFT
- EXPECTED DRIFT
- UNDOCUMENTED DRIFT
- BASELINE ERROR
- UNKNOWN

## Output

`docs/reverse-engineering/drift/<baseline-or-date>-drift-review.md`

Do not automatically rewrite baseline. Report drift first for review.
