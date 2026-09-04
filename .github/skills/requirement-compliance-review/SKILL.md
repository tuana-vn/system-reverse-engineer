---
name: requirement-compliance-review
description: Compare a user/customer requirement against a patch's reconstructed implemented behavior and the current-system baseline. Use to determine whether development is correct, complete, over-scoped, or likely to regress unrelated behavior.
---

# Requirement vs Implementation Compliance

## Inputs

- requirement/specification
- patch/diff
- patch impact review if available
- current baseline memory

## Normalize Requirement

Create atomic rules `R-001`, `R-002`, ...

For each capture:

- actor/trigger
- preconditions
- expected rule
- expected result
- failure/exception behavior
- compatibility requirement
- ambiguity

Do not invent acceptance criteria.

## Requirement Fidelity Gate

For every normalized mandatory field/behavior/condition, point to the exact authoritative requirement
clause that requires it. If no clause exists, it must not be represented as a requirement obligation.
It may appear only as an explicitly labeled `PROPOSED` design option/guidance.

Required threshold:

```text
UNSUPPORTED_REQUIREMENT_EXPANSION = 0
```

Before a ready/pass verdict, reconcile executive summaries and aggregate counts with the row-level
matrix. A claim such as "all requirements fail" is invalid when any matrix row is PASS/NO_GAP.

## Compare

Use implementation rules from the patch impact review where possible.

Central matrix:

| Req ID | Expected Behavior | Implemented Behavior | Status | Gap | Risk | Evidence |
|---|---|---|---|---|---|---|

Statuses:

- PASS
- PARTIAL
- FAIL
- NOT IMPLEMENTED
- OVER-IMPLEMENTED
- UNKNOWN

## Detect

- missing conditions
- missing branches
- wrong defaults
- over-broad changes
- compatibility regressions
- requirement ambiguity
- wrong integration/client selection
- error-path mismatch
- observability/audit mismatch

## Overall Verdict

Use:

- COMPLIANT
- MOSTLY COMPLIANT
- PARTIALLY COMPLIANT
- NON-COMPLIANT
- CANNOT VERIFY

## Output

`docs/reverse-engineering/reviews/<patch>-requirement-compliance.md`

Never update baseline memory from an unmerged patch.
