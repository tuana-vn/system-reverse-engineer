---
name: wbs-verification
description: Independently verify an implementation WBS for completeness, traceability, dependency correctness, source/design consistency, verification coverage, and missing work. Use before implementation readiness certification.
license: MIT
---

# WBS Verification

## Mission

Do not only review tasks that exist.
Actively search for missing implementation work.

## Inputs

- authoritative requirement
- verified gap analysis
- verified TDD
- artifact registry
- verified detailed designs
- detailed-design verification reports
- WBS
- test design/current source

## 1. Backward Trace Every Task

Every WBS task must map to:

```text
Requirement
→ Gap
→ TDD Decision
→ Design Artifact
→ Verified DD
→ WBS Task
```

Tasks with no approved design basis are:

`UNAPPROVED_WORK`


## 1A. Exhaustive WBS ↔ Artifact Semantic Identity

Run this check for **every WBS task**, not a sample.

For each WBS row, derive the task's primary implementation deliverable from its title/objective and
compare it with:

```text
referenced Artifact ID
→ canonical registry artifact name
→ registry responsibility/scope
→ VERIFIED DD owned implementation unit(s)
```

A PASS requires semantic identity, not just link existence.

Create:

| WBS ID | Task / Primary Deliverable | Artifact ID | Canonical Artifact Name | Registry Responsibility | DD-Owned Unit | Match? | Finding |
|---|---|---|---|---|---|---:|---|

Hard rules:

- If task A references Artifact B but Artifact B owns a different primary implementation unit, mark:
  `WBS_ARTIFACT_SEMANTIC_MISMATCH`.
- A symbol appearing somewhere in the TDD/DD is not enough to re-label the artifact.
- The canonical artifact name/responsibility comes from the design artifact registry; do not invent
  a different semantic label for the same Artifact ID in another section.
- If a subordinate class/type is intended to belong to an artifact, ownership must be explicit in
  the registry or VERIFIED DD scope. Mere `@see`, mention, dependency, or cross-reference is not
  ownership.
- Any HIGH/CRITICAL semantic mismatch blocks `WBS_VERIFIED`.

Required threshold:

```text
all WBS task semantic mappings valid = 100%
```

## 2. Forward Coverage Every Design Artifact

For every `DD_VERIFIED` artifact ask:

- production/config/data changes covered?
- callers/consumers affected by signature/contract change covered?
- integration changes covered?
- migration/compatibility work covered?
- tests covered?
- docs/config samples covered if required?

Missing work is a first-class finding.

## 3. Source-Side Missing Work Search

Use current source to search likely affected surfaces implied by the verified design:

- callers/references
- implementations
- constructors/factories/DI
- serializers/mappers
- config consumers
- migrations/schema
- tests/fixtures
- generated/config files
- integration adapters
- sibling operations that must preserve behavior

Do not add a task unless the design/source evidence supports the impact.

## 4. Dependency Verification

Check:

- dependency direction
- prerequisites
- circular dependency
- sequencing of interface vs consumer changes
- migration/config sequencing
- test fixture/setup prerequisites

## 5. Done-Criteria Verification

Done criteria must be observable and verifiable.

Reject vague criteria like:
- "works correctly"
- "update code"
- "test as needed"

Prefer:
- build/test target
- exact contract behavior
- artifact/test IDs
- source-visible state

## 6. Test / Verification Coverage

Every changed external contract and HIGH/CRITICAL behavior must have concrete verification.

Do not accept unit-only coverage for externally visible changes when higher-level proof is feasible.

## 7. Verification Matrix

| Finding ID | WBS / Artifact | Finding | Evidence | Severity | Required Correction |
|---|---|---|---|---|---|

## 8. Gate

Before `WBS_VERIFIED`:

```text
[ ] every task has approved design traceability
[ ] every task's primary deliverable semantically matches its referenced artifact responsibility / DD-owned unit
[ ] semantic identity verification was executed for 100% of WBS tasks
[ ] every verified design artifact has complete task coverage
[ ] source-side missing-work search completed
[ ] dependency DAG is implementable
[ ] every code-changing task has verification
[ ] external contract changes have appropriate higher-level tests
[ ] done criteria are concrete
[ ] no unresolved HIGH/CRITICAL WBS gap remains
```

Overall:

- WBS_VERIFIED
- WBS_PARTIALLY_VERIFIED
- WBS_INCOMPLETE
- WBS_BLOCKED_SOURCE_GAP

## Output

Use the active workflow-declared WBS verification output path. Do not reuse legacy WBS verification artifacts.


# 4.0 WBS / Effort Separation Gate

WBS is not effort estimation.

If the WBS contains any implementation effort estimate such as:

- hours
- person-days
- story points
- "~1 week"
- duration estimates attached to tasks/phases

record:

`WBS_CONTAINS_UNAPPROVED_EFFORT_ESTIMATE`

and do NOT return `WBS_VERIFIED`.

Effort estimation requires a separate explicitly-invoked capability and evidence model.
