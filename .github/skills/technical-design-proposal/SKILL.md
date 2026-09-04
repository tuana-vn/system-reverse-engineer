---
name: technical-design-proposal
description: Produce a reviewer-grade, source-backed technical design with mandatory static architecture, runtime architecture, component responsibilities, traceability, provenance, compatibility, and exact change points. Use only after current-state and verified-gap analysis.
license: MIT
---

# Technical Design Proposal — 4.0

## Purpose

A Technical Design must explain BOTH:

```text
WHAT the proposed system structure is
AND
HOW the proposed runtime behavior works
```

A TDD that contains only prose, gap tables, or sequence flows is incomplete when the change
affects software structure or responsibilities.

Use:

```text
Requirement
→ Current Source / Runtime Evidence
→ Verified Gap
→ Proposed Static Architecture
→ Proposed Dynamic Architecture
→ Detailed Responsibilities / Contracts
→ Change Set
→ Verification
```

## Source-of-Truth Rules

Clearly separate:

- CURRENT VERIFIED BEHAVIOR
- REQUIREMENT / INTENDED BEHAVIOR
- VERIFIED GAP
- PROPOSED DESIGN
- ASSUMPTION
- OPEN QUESTION / SOURCE_NOT_RESOLVED

Current repository source is authoritative for CURRENT structure and behavior.
Requirement is authoritative for intended behavior.
A proposed class/interface/component is never a current-source fact.

When used after compliance/impact analysis:

- design only VERIFIED gaps
- do not redesign behavior already proven compliant
- do not convert secondary concerns into requirement gaps
- if a design decision depends on unresolved source evidence, use `TDD_NOT_READY_SOURCE_GAPS`

---

# 1. Canonical Requirement / Scope Matrix

When behavior is operation/surface-specific, include:

| Rule ID | Surface / Operation | Applies? | Condition | Required Observable Behavior | Explicit Exclusion |
|---|---|---:|---|---|---|

Rules:

- evaluate each row independently
- no condition leakage between endpoints/operations
- preserve MUST-NOT/non-goals
- do not widen requirement scope

---

# 2. CURRENT Static Architecture — Mandatory When Relevant

Use the exact heading:

```text
## CURRENT Static Architecture
```

Include a Mermaid `classDiagram` or component diagram showing only source-verified existing
classes/interfaces/components that are relevant to the change.

Show where materially relevant:

- controllers/resources/handlers
- services/use cases
- interfaces and implementations
- integration adapters/clients
- data/context models
- repositories/configuration components
- external boundaries

Rules:

- no proposed type in CURRENT diagram
- uncertain relationship must be labeled UNKNOWN or omitted
- use exact current source names
- diagram must be explainable from source evidence

If the feature is structurally trivial and no meaningful current static view exists, explicitly state
why `CURRENT Static Architecture` is not applicable. Do not omit the section silently.

---

# 3. PROPOSED Static Architecture — HARD REQUIREMENT

Use the exact heading:

```text
## PROPOSED Static Architecture
```

This section is a required TDD artifact.

When the design introduces or materially changes classes/interfaces/components/responsibilities,
include a Mermaid static diagram.

Prefer:

```mermaid
classDiagram
```

when class/interface relationships matter.

Use component-style Mermaid when module/package/system boundaries are clearer.

The proposed static architecture must show:

- important EXISTING types/components that remain involved
- every major NEW type/component
- every materially MODIFIED existing type/component
- interfaces and implementations
- important dependency/composition relationships
- important callers/consumers
- external boundaries where relevant
- the same names used by the written design

Mark proposed artifacts clearly, for example with `<<PROPOSED>>` or explicit labels.

Do NOT invent extra classes just to make the picture symmetrical.

### Non-structural changes

Even when no new class/interface is required, keep the `PROPOSED Static Architecture` section.
Show the resulting static structure or explain, with evidence, why the static structure is unchanged
and identify which existing responsibilities are modified.

### Hard completeness rule

If the design changes structural responsibilities and `PROPOSED Static Architecture` is missing:

```text
TDD = INCOMPLETE
```

Do not issue `TDD_READY`.

---

# 4. Component Responsibilities — Mandatory

Use the exact heading:

```text
## Component Responsibilities
```

Create:

| Component / Type | Existing / Proposed | Responsibility | Inputs | Outputs / Result | Dependencies | Requirement / Gap |
|---|---|---|---|---|---|---|

Every major type shown in the proposed static diagram must appear here.

---

# 5. Class / Interface / Contract Design

When applicable, define:

- proposed/existing class or interface
- purpose
- methods / pseudo-signatures in repository language
- caller(s)
- lifecycle/ownership
- inputs/outputs
- error/result contract
- concurrency/threading only if relevant
- sensitive-data constraints where relevant

Do not fabricate exact signatures if the design evidence only supports conceptual parameters.
Mark conceptual signatures as `PROPOSED PSEUDO-SIGNATURE`.

---

# 6. PROPOSED Dynamic Architecture / Runtime Sequences

Use the exact heading:

```text
## PROPOSED Dynamic Architecture / Runtime Sequences
```

When runtime behavior changes, include Mermaid sequence/flow diagrams.

At minimum cover where applicable:

- primary success
- primary functional rejection/failure
- technical error/failure
- important MUST-NOT / excluded flow
- retry/fallback flow

Sequence diagrams do NOT replace static architecture.

---

# 7. Current → Proposed Flow Comparison

For materially changed flows:

```text
CURRENT:
entry
→ current decision/integration
→ current observable result

PROPOSED:
same entry
→ minimal new/changed decision point
→ proposed integration/behavior
→ preserved or changed observable result
```

This prevents architecture diagrams from becoming disconnected pictures.

---

# 8. Field / Data / Context Provenance

For every verified gap involving externally meaningful data:

```text
trigger
→ source/retrieval
→ parse/decode
→ transform/normalize
→ mapping/state
→ serialization/emission
→ observable result
```

For proposed behavior:

```text
CURRENT provenance
→ proven break point
→ proposed change
→ resulting provenance
```

Do not add output-layer conditions when earlier retrieval/mapping already enforces the behavior.

---

# 9. Boundary → Exposure Coverage

When a changed design touches an integration/downstream boundary:

```text
boundary
← ALL direct invocation/construction sites
← ALL material caller chains
← ALL external entry points / proven internal roots
```

The design must account for all materially impacted external operations.
Do not design for one representative endpoint only.

---

# 10. Candidate Design Evaluation

When there are materially different viable placements/approaches:

| Candidate | Requirement Coverage | Exclusion Safety | Evidence Support | Coupling | Duplicate Risk | Compatibility | Change Size | Decision |
|---|---|---|---|---|---|---|---|---|

Choose based on source-backed fit, not architectural fashion.

---

# 11. Gap → Solution Matrix

| Gap ID | Surface | Current Observable Behavior | Required Behavior | Proven Break Point | Minimal Proposed Change | Evidence |
|---|---|---|---|---|---|---|

Every proposed change must map to a verified gap or explicit requirement-enabling design need.

---

# 12. Integration / Existing Change Point Table

| Existing File / Class / Method | Current Role | Proposed Change | Why This Point | Risk | Evidence |
|---|---|---|---|---|---|

Use exact source anchors where possible.

---

# 13. Data Model / Configuration / Persistence

Include only when affected.

For data model:
- field/type
- provenance
- nullability/default
- serialization/persistence
- compatibility

For configuration:
- source/default/override precedence
- consumer
- invalid/missing behavior
- lifecycle/reload

For persistence:
- schema/key
- read/write path
- consistency/transaction behavior
- migration/backward compatibility

---

# 14. Error / Failure / Isolation Design

Define:

- functional rejection
- technical failure
- mapping to existing observable behavior
- retry/fallback if applicable
- failure-isolation rules
- whether new supporting logic may mask original behavior

---

# 15. Compatibility / Non-Goal Preservation

Explicitly cover:

- unaffected operations
- MUST-NOT behavior
- protocol/API compatibility
- existing success/error behavior
- performance-sensitive call-count/data-volume changes
- sensitive-data handling
- internal/background behavior where relevant

---

# 16. Exact Proposed Change Set

| Change ID | Artifact | Existing / Proposed | File / Proposed Location | Change | Requirement IDs | Gap IDs | Verification |
|---|---|---|---|---|---|---|---|

No change item without traceability.

---

# 17. Design Traceability

| Requirement | Verified Gap | TDD Decision | Static Architecture Component | Runtime Flow | Change ID | Test / Verification |
|---|---|---|---|---|---|---|

This is the bridge from requirement to implementation planning.

---

# 18. Diagram Consistency Gate

Before completion, verify:

```text
[ ] CURRENT Static Architecture section exists
[ ] PROPOSED Static Architecture section exists
[ ] proposed diagram includes every major new/modified component
[ ] Component Responsibilities covers every major proposed diagram component
[ ] class/interface design uses the same names as the diagram
[ ] runtime diagrams use the same components/responsibilities
[ ] exact change set uses the same names/locations
[ ] external boundaries are represented correctly
[ ] CURRENT diagram contains no proposed artifacts
[ ] proposed-vs-existing distinction is explicit
```

Any applicable failure means the TDD is not ready.

---

# 19. TDD Completion Gate

Before `TDD_READY`:

```text
[ ] requirement/scope rows are isolated
[ ] verified gaps are separate from assumptions
[ ] current behavior is source-backed
[ ] CURRENT Static Architecture present or explicitly justified N/A
[ ] PROPOSED Static Architecture present or explicitly justified unchanged
[ ] Component Responsibilities present
[ ] dynamic/runtime diagrams cover materially changed flows
[ ] changed field/data provenance is proven where applicable
[ ] boundary/exposure coverage is complete where applicable
[ ] proposed change targets proven break points
[ ] compatibility/non-goals are preserved
[ ] exact change set is traceable
[ ] tests/verification map to observable behavior
[ ] no unresolved HIGH/CRITICAL source-resolvable design gap remains
```

Statuses:

- `TDD_READY`
- `TDD_READY_WITH_EXTERNAL_BLOCKERS`
- `TDD_NOT_READY_SOURCE_GAPS`
- `TDD_INCOMPLETE_ARCHITECTURE`

## Output

`docs/reverse-engineering/proposals/<feature>-tdd.md`

Do not update canonical current-system baseline.
