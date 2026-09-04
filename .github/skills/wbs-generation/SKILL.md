---
name: wbs-generation
description: Generate a traceable implementation Work Breakdown Structure from verified detailed-design artifacts, current source anchors, requirement/TDD traceability, dependencies, and verification obligations. Use only after detailed designs are verified.
license: MIT
---

# Implementation WBS Generation

## Purpose

WBS is WHAT must be implemented, not an effort estimate.

Do not jump from TDD prose directly to generic tasks.

Inputs must include VERIFIED detailed designs.

```text
Requirement
→ Gap
→ TDD
→ Design Artifact
→ VERIFIED Detailed Design
→ WBS Task
→ Verification
```

## Inputs

- authoritative requirement
- verified gap analysis
- verified TDD
- design artifact registry
- all `DD_VERIFIED` detailed designs
- detailed-design verification reports
- test design if available
- current repository

## 1. Task Derivation

Derive tasks only from verified design decisions.

Task categories:

- production code
- API/contract
- integration
- data/persistence
- configuration
- migration/compatibility
- tests
- build/deployment
- documentation
- cleanup only if required by approved design

Do not add "nice to have" refactoring.

## 2. Task Granularity

A task should be small enough to have:

- one clear outcome
- concrete source/design anchors
- explicit dependencies
- verifiable done criteria

But do not split mechanical edits into dozens of meaningless microtasks.

## 3. Stable IDs

Use:

`WBS-001`, `WBS-002`, ...


## 3A. WBS ↔ Design Semantic Identity

Traceability is not satisfied merely because a WBS row contains an existing Artifact ID.

For every WBS task, identify its **primary implementation deliverable** and prove that the
referenced design artifact(s) own that deliverable.

Required semantic chain:

```text
WBS task title / objective / primary deliverable
↔ registry artifact name + responsibility
↔ VERIFIED DD owned implementation unit(s)
↔ TDD design decision
```

Rules:

1. An Artifact ID reference is necessary but not sufficient.
2. A type/class/interface being merely mentioned, imported, referenced, or linked from a DD does
   **not** prove that the artifact owns that implementation unit.
3. If a WBS task's primary deliverable is a subordinate type, one of these must be true:
   - the registry/DD explicitly declares that subordinate type inside the owning artifact scope, or
   - the design artifact decomposition must be revised to track it separately.
4. Do not map a task titled for component/type A to an artifact whose registered responsibility is
   component/type B unless the artifact explicitly owns A.
5. If semantic ownership cannot be proven, stop with `WBS_BLOCKED_DESIGN_GAP`; do not manufacture a
   mapping from nearby TDD prose.

Before emitting the WBS, create an internal/exposed consistency table:

| WBS ID | Primary Deliverable | Referenced Artifact IDs | Registry Responsibility | DD-Owned Unit | Semantic Match? | Evidence |
|---|---|---|---|---|---:|---|

Required threshold:

```text
WBS ↔ artifact semantic identity = 100%
```

## 4. WBS Table

| WBS ID | Design Artifact IDs | Task | Existing Source Anchor / Proposed Location | Change Type | Dependencies | Requirement IDs | TDD/DD References | Verification | Done Criteria |
|---|---|---|---|---|---|---|---|---|---|

Change Type:

- ADD
- MODIFY
- REMOVE
- CONFIGURE
- MIGRATE
- TEST
- DOCUMENT
- VERIFY

## 5. Dependency DAG

Derive implementation ordering from artifact dependencies and code/runtime dependencies.

Create:

| WBS ID | Depends On | Dependency Reason | Hard/Soft |
|---|---|---|---|

Detect circular dependency.

Do not invent ordering solely from file order.

## 6. Verification Mapping

Every code-changing task needs a verification path.

Map to:
- existing test to update
- new test ID/viewpoint
- source/build verification
- runtime/integration verification
- manual verification only when automation is not feasible

## 7. Traceability

Create:

| Requirement ID | Gap ID | TDD Decision ID | Artifact ID | DD | WBS IDs | Test/Verification IDs | Coverage |
|---|---|---|---|---|---|---|---|

No verified design artifact may be orphaned.

## 8. WBS Gate

Before `WBS_READY_FOR_VERIFICATION`:

```text
[ ] all DD_VERIFIED artifacts have implementation/verification task coverage
[ ] every WBS task maps back to verified design
[ ] every WBS task primary deliverable semantically matches the responsibility/owned unit of its referenced artifact(s)
[ ] no task relies on a merely-mentioned DD/TDD symbol as proof of artifact ownership
[ ] source anchors/proposed locations are concrete
[ ] dependencies are explicit
[ ] code-changing tasks have done criteria and verification
[ ] config/migration/docs/test work is included when required
[ ] no unapproved architecture/refactoring was added
[ ] no HIGH/CRITICAL source gap is hidden inside a task
```

Statuses:

- WBS_READY_FOR_VERIFICATION
- WBS_BLOCKED_DESIGN_GAP
- WBS_BLOCKED_SOURCE_GAP

## Important

Do NOT estimate hours/days/story points in this skill.
Effort estimation is a separate concern.
