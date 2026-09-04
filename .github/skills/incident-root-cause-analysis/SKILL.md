---
name: incident-root-cause-analysis
description: Analyze production or test incidents using logs and symptoms together with the reconstructed architecture. Use to localize failures, build timelines, test hypotheses, and distinguish evidence from speculation.
---

# Incident / Root-Cause Analysis

## Rules

Do not jump from symptom to root cause.

Separate:

- incident observations
- architectural facts
- hypotheses
- verified root cause

## Build Expected Flow

Use current architecture to reconstruct the expected path for the affected operation.

## Timeline

| Time | Layer | Event | Evidence |
|---|---|---|---|

## Localize Failure

Consider:

- before downstream boundary
- routing/selection
- request/command construction
- downstream execution
- response parsing
- retry/fallback
- internal mapping
- final response

## Hypotheses

| Hypothesis | Supporting Evidence | Contradicting Evidence | Confidence | Verification Needed |
|---|---|---|---|---|

Do not label root cause VERIFIED unless direct evidence supports it.

## Output

`docs/reverse-engineering/incidents/<incident>-analysis.md`

Do not mutate baseline memory from incident hypotheses.
