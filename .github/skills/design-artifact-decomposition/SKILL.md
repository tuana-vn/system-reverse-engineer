---
name: design-artifact-decomposition
description: Decompose a verified technical design into a complete, source-traceable registry of implementation-relevant design artifacts and dependencies. Use after TDD verification and before detailed design or WBS generation.
license: MIT
---

# Design Artifact Decomposition

## Purpose

Do not jump directly from a TDD to a task list.

First convert the TDD into an explicit registry of design artifacts:

```text
Requirement
→ Verified Gap
→ Verified TDD Decision
→ Design Artifact Registry
```

The registry is the source of truth for detailed-design coverage.

## Inputs

- authoritative requirement
- verified gap analysis
- VERIFIED technical design
- TDD verification report
- current repository
- test design if already available

## Artifact Types

Use the smallest meaningful technology-neutral type:

- CLASS / INTERFACE
- MODULE / COMPONENT
- API CONTRACT
- DATA MODEL
- CONFIGURATION
- PERSISTENCE
- INTEGRATION
- RUNTIME FLOW
- STATE MACHINE
- ERROR HANDLING
- SECURITY
- OBSERVABILITY / AUDIT
- TEST SUPPORT
- MIGRATION / COMPATIBILITY
- DOCUMENTATION
- OTHER

Do not force Java/REST concepts onto non-Java/non-REST systems.

## 1. Extract TDD Decisions

Assign stable IDs:

`TD-001`, `TD-002`, ...

Every material design decision must be represented.

## 2. Derive Artifacts

Assign:

`DA-001`, `DA-002`, ...

Each artifact must represent one cohesive implementation/design responsibility.

Do not create artifacts merely because a file exists.
Do not merge unrelated responsibilities only to reduce artifact count.


## 2A. Proposed Unit Ownership Closure

Before finalizing artifact boundaries, enumerate all implementation-significant PROPOSED units
from the VERIFIED TDD.

For each unit assign exactly one ownership disposition:

```text
DEDICATED_ARTIFACT
or
SUBORDINATE_TO:<ART-ID>
```

`SUBORDINATE_TO` is valid only when the owning artifact responsibility explicitly includes the
subordinate unit. Do not hide a distinct implementation responsibility inside an unrelated
artifact merely to avoid another ART ID.

Create:

| Proposed Unit | TDD Evidence | Responsibility | Ownership Disposition | Owning ART-ID | Why Ownership Is Valid | Covered? |
|---|---|---|---|---|---|---:|

Required threshold:

```text
PROPOSED_UNIT_OWNERSHIP_COVERAGE = 100%
```

If any significant proposed unit has no valid explicit owner:

`ARTIFACT_DECOMPOSITION_INCOMPLETE`

Do not proceed to DD generation.

### Boundary Rule

Artifact decomposition is responsibility-based, not "one class = one artifact".

A dedicated artifact is warranted when a unit has materially independent responsibility,
contract, lifecycle, dependency boundary, failure semantics, state/config ownership, or
verification obligation.

A subordinate unit is acceptable only when that ownership is explicit.

## 3. Existing vs Proposed

For each artifact classify:

- EXISTING_MODIFIED
- PROPOSED_NEW
- EXISTING_UNCHANGED_REFERENCE

For existing artifacts verify source anchors.
For proposed artifacts state the proposed ownership/location without pretending it exists.

## 4. Dependency Graph

Record dependencies:

```text
DA-A requires DA-B
```

Classify dependency:

- API/CONTRACT
- DATA
- RUNTIME
- CONFIGURATION
- BUILD
- TEST
- MIGRATION
- ORDERING

Detect obvious circular dependency in the proposed implementation order.
If architectural circularity is intentional, explain it rather than hiding it.

## 5. Design Artifact Registry


For every artifact, the registry must explicitly record its owned proposed units, including
subordinate units.

Recommended field:

```text
Owned Proposed Units:
- <primary unit>
- <explicit subordinate unit>
```

The registry is the canonical owner map used by DD, WBS, and later verification.



Required table:

| Artifact ID | Name | Type | Requirement IDs | Gap IDs | TDD Decision IDs | Existing/Proposed | Source Anchor / Proposed Location | Dependencies | DD Status | DD Verification | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|

Initial statuses:

```text
DD Status = NOT_STARTED
DD Verification = NOT_VERIFIED
```

## 6. Coverage Matrix

Create:

| Requirement ID | Gap ID | TDD Decision ID | Artifact IDs | Covered? | Evidence |
|---|---|---|---|---:|---|

No verified TDD decision may be orphaned.

## 7. Completion Gate


### Proposed Unit Ownership Completion

Before `ARTIFACT_REGISTRY_READY`:

- every implementation-significant proposed unit has exactly one owner
- every subordinate unit is explicitly named under the owning artifact
- no proposed unit is owned only by implication
- ownership coverage = 100%

Otherwise:

`ARTIFACT_DECOMPOSITION_INCOMPLETE`



Before `ARTIFACT_REGISTRY_READY`:

```text
[ ] every material verified TDD decision has artifact coverage
[ ] every artifact maps backward to TDD/requirement/gap
[ ] existing source anchors are verified where applicable
[ ] proposed artifacts are explicitly marked
[ ] dependencies are recorded
[ ] no obvious implementation-relevant TDD decision is hidden in prose
[ ] no source-resolvable HIGH/CRITICAL decomposition ambiguity remains
```

Statuses:

- ARTIFACT_REGISTRY_READY
- ARTIFACT_REGISTRY_PARTIAL
- ARTIFACT_REGISTRY_BLOCKED
- ARTIFACT_DECOMPOSITION_INCOMPLETE

## Output

Use the active workflow-declared registry output path. Do not invent or reuse a legacy shared registry filename.


<!-- workflow-status-contract:start -->
```yaml
emitted_statuses:
  - ARTIFACT_REGISTRY_READY
  - ARTIFACT_REGISTRY_PARTIAL
  - ARTIFACT_REGISTRY_BLOCKED
  - ARTIFACT_DECOMPOSITION_INCOMPLETE
```
<!-- workflow-status-contract:end -->


# 4.0 Registry Evidence Contract

`ARTIFACT_REGISTRY_READY` is invalid unless the artifact contains BOTH:

## Proposed Unit Inventory

| Proposed Unit | Type | TDD Evidence | Implementation-Significant? | Reason |
|---|---|---|---:|---|

This inventory is unit-centric, not artifact-centric.

## Proposed Unit Ownership Closure

| Proposed Unit | Ownership Disposition | Owning ART-ID | Explicit Responsibility Text | Coverage |
|---|---|---|---|---:|

Required:

```text
inventory rows >= 1 when TDD proposes implementation units
ownership rows == inventory rows
coverage = 100%
unowned units = 0
```

An artifact list that merely maps ART IDs to themselves is NOT an ownership closure.

Do not emit `ARTIFACT_REGISTRY_READY` without these tables.
