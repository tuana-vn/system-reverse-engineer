---
name: implementation-readiness-certification
description: Certify whether a requirement-driven change is ready for implementation by verifying the complete traceability chain from requirement through gap analysis, TDD, design artifacts, verified detailed designs, WBS, and tests, with no unresolved source-resolvable high-impact gaps.
license: MIT
---

# Implementation Readiness Certification

## Purpose

Implementation readiness is not "the documents look complete".

Certify the full chain:

```text
REQ
→ GAP
→ TDD
→ DESIGN ARTIFACT
→ VERIFIED DD
→ VERIFIED WBS
→ TEST / VERIFICATION
```

## Inputs

- requirement
- current-state analysis
- gap/compliance analysis
- TDD + verification
- artifact registry
- all detailed designs + verification reports
- WBS + verification
- contract/regression test design
- open-question/evidence state

## 1. Traceability Closure

Required matrix:

| Requirement ID | Gap ID | TDD Decision | Artifact ID | DD | WBS IDs | Test IDs | Status |
|---|---|---|---|---|---|---|---|

No material requirement/gap may be orphaned.

## 2. Evidence Health

Check:

- current-source anchors still exist
- no high-impact claim relies only on stale generated prose
- no unresolved provenance/exposure gap affects implementation
- no source-resolvable HIGH/CRITICAL open question remains
- external blockers are named precisely

## 3. Design Health

Check:

- TDD verified
- all implementation-relevant artifacts registered
- all required artifacts DD_VERIFIED
- proposed-vs-existing boundaries clear
- compatibility/non-goals preserved

## 4. Plan Health

Check:

- WBS_VERIFIED
- dependencies implementable
- missing-work search completed
- tests/verification mapped
- done criteria concrete

## 5. Certification

Use exactly one:

- IMPLEMENTATION_READY
- IMPLEMENTATION_READY_WITH_EXTERNAL_BLOCKERS
- NOT_READY_DESIGN_GAPS
- NOT_READY_WBS_GAPS
- NOT_READY_SOURCE_GAPS

Rules:

`IMPLEMENTATION_READY` requires:

```text
unresolved source-resolvable CRITICAL = 0
unresolved source-resolvable HIGH = 0
unverified required DD artifacts = 0
HIGH/CRITICAL WBS findings = 0
material requirement traceability gaps = 0
```

External blockers may remain only when current repository/source cannot resolve them and
the exact external evidence/dependency is named.

## Output

Use the active workflow-declared implementation-readiness output path. Do not reuse legacy readiness artifacts.


# 4.0 WBS Purity Check

Before `IMPLEMENTATION_READY`, verify the WBS contains no effort/duration estimates unless an
explicit separate effort-estimation artifact is an approved input.

If unauthorized effort estimates are present:

`NOT_READY_WBS_GAPS`

Reason:
`WBS_CONTAINS_UNAPPROVED_EFFORT_ESTIMATE`
