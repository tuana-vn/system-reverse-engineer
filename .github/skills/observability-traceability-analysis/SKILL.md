---
name: observability-traceability-analysis
description: Analyze whether a system has enough evidence to trace an operation across internal layers and external boundaries, identify troubleshooting blind spots, and design or review audit/log traceability without confusing logs with source-of-truth architecture.
---

# Observability and Traceability Analysis

## Core Goal

For a selected operation, determine whether support can reconstruct:

```text
Inbound request/event
→ business operation
→ routing decision
→ concrete implementation
→ external interaction
→ external result/error
→ internal result
```

## Traceability Dimensions

At each step inspect:

- timestamp
- request/operation identity
- target/entity identity
- business operation
- selected implementation
- mode/config context
- downstream command/API operation
- downstream-generated identifiers if naturally available
- result/error
- duration

Do not assume custom IDs can be propagated to external systems.

## Gap Matrix

| Flow Step | Existing Evidence | Missing Evidence | Troubleshooting Impact | Proposed Improvement |
|---|---|---|---|---|

Classify:

- TRACEABLE
- PARTIALLY TRACEABLE
- BLIND SPOT

## Important Distinction

- Source code establishes architectural behavior.
- Audit/log records establish what happened in a particular execution.
- Neither should be mistaken for the other.

## Output

`docs/reverse-engineering/observability/<scope>-traceability-analysis.md`


## 4.0 Source-of-Truth Constraint

Do not promote architecture claims merely because logs show one execution.

Runtime logs prove execution truth for that instance.
Source/wiring proves architectural behavior.

Cross-reference both when possible.
