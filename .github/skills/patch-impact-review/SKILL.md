---
name: patch-impact-review
description: Review a patch or Git diff against the evidence-backed current-system baseline, reconstruct its business purpose and implemented behavior, trace architectural impact, identify regression risks, and produce a reusable implementation summary.
license: MIT
---

# Patch Architectural Impact Review

## Baseline Safety

A patch is proposed behavior until proven merged.

Do not update current baseline memory.

## Inputs

- patch/diff
- compact reverse-engineering memory
- relevant detailed source/docs only

## Reconstruct Three Levels

### Business Purpose
Why the change appears necessary.

### Functional Behavior
What observable/business behavior changes.

### Technical Implementation
How the code implements that behavior.

For bug fixes:

```text
Observed/Reported Problem
→ PATCH-IMPLIED ROOT CAUSE
→ Changed Logic
→ Expected Corrected Behavior
```

Label patch-implied root cause unless independently verified.

## Trace Impact

Map relevant changes onto the actual runtime flow.

Check:

- inbound contract
- business rules
- routing/client selection
- external integrations
- configuration
- error/retry/fallback
- lifecycle/concurrency
- security
- audit/observability
- compatibility

## Hidden Impact

Inspect callers, overrides, factories, config consumers, shared utilities, and tests around changed symbols.

## Required Tables

### Changed Surface

| File | Symbol | Change | Runtime Role |
|---|---|---|---|

### Before vs After

| Scenario | Baseline | Patched | Confidence | Evidence |
|---|---|---|---|---|

### Risks

| Risk | Scenario | Severity | Likelihood | Evidence | Test |
|---|---|---|---|---|---|

## Implementation Behavior Summary

Create concise implementation rule IDs:

| Rule ID | Trigger/Precondition | Implemented Rule | Result/Side Effect | Failure Behavior | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Output

`docs/reverse-engineering/reviews/<patch>-impact-review.md`
