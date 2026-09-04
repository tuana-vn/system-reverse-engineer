---
name: artifact-detailed-design
description: Produce a source-backed detailed design for exactly one registered design artifact at a time, preserving requirement/TDD traceability, current-source anchors, runtime/data provenance, compatibility, and explicit proposed-vs-existing boundaries.
license: MIT
---

# Artifact Detailed Design

## Purpose

Detailed design is generated per registered artifact, not as an unconstrained rewrite of the TDD.

One run handles exactly one Artifact ID.

```text
Requirement
→ Gap
→ TDD Decision
→ Artifact Registry Entry
→ Detailed Design
```

## Inputs

Required:

- Artifact ID
- design artifact registry
- verified TDD
- TDD verification report
- requirement/gap artifacts
- current repository

Use test design when it clarifies verification obligations.

## 1. Reverify Artifact Context

Before designing:

- verify the Artifact ID exists in registry
- verify its requirement/gap/TDD mappings
- reverify existing source anchors
- load direct dependencies
- check whether dependency designs are required first

If a prerequisite artifact is unresolved and blocks design:

`DD_BLOCKED_DEPENDENCY`

## 2. Separate Existing / Proposed / Unknown

Use explicit sections:

```text
CURRENT SOURCE-BACKED
PROPOSED
UNKNOWN / SOURCE GAP
```

Never describe a proposed class/module/method as existing.

## 3. Generic Core Design

For every artifact define:

- responsibility
- scope / non-goals
- source anchors or proposed location
- dependencies
- public/internal contract
- inputs/outputs/state
- runtime behavior
- error/failure behavior
- configuration/lifecycle where applicable
- compatibility constraints
- concurrency/threading only when source/design makes it relevant
- security/sensitive-data considerations only when relevant
- verification obligations

## 4. Type-Specific Design

### CLASS / INTERFACE / MODULE / COMPONENT

Include:
- existing/proposed signatures
- callers/consumers
- dependencies
- lifecycle/ownership
- exceptions/results
- before/after relationships

### API CONTRACT

Include:
- method/operation
- request inputs
- validation/combination rules
- response/output
- error contract
- compatibility

### DATA MODEL

Include:
- fields/types
- source/provenance
- nullability/default
- serialization/persistence
- sensitive-data classification
- compatibility

### CONFIGURATION

Include:
- source/default/override precedence
- consumer
- reload/lifecycle
- invalid/missing behavior
- backward compatibility

### INTEGRATION

Include:
- operation/request construction
- routing/selection
- result/error semantics
- timeout/retry/fallback
- data provenance
- all exposure paths materially affected

### RUNTIME FLOW / STATE MACHINE

Include:
- triggers
- states/branches
- transitions
- data/context propagation
- side effects
- success/failure paths
- before/after Mermaid

### PERSISTENCE

Include:
- schema/object/key
- read/write paths
- transaction/consistency semantics
- migration/backward compatibility

### ERROR HANDLING

Include:
- source error
- translation
- observable error
- preservation/masking rules

Other types should use the same evidence-first principle and explain type-specific details.

## 5. Provenance and Exposure

When applicable include:

```text
field/data provenance:
trigger → source → transform → mapping/state → output

boundary/exposure:
boundary ← all material invocation sites ← external/internal roots
```

Do not omit these because the artifact appears "internal".

## 6. Proposed Change Table

| DD Item | Existing Source Anchor | Current Behavior | Proposed Behavior | Requirement/Gap/TDD | Risk | Verification |
|---|---|---|---|---|---|---|

## 7. Detailed Design Gate

Before `DD_READY_FOR_VERIFICATION`:

```text
[ ] artifact registry mappings preserved
[ ] existing source anchors reverified
[ ] proposed artifacts/methods clearly marked
[ ] runtime behavior is concrete enough to implement
[ ] field/data provenance covered where applicable
[ ] boundary/exposure covered where applicable
[ ] error/failure behavior defined
[ ] compatibility/non-goals preserved
[ ] dependencies identified
[ ] verification obligations identified
[ ] no HIGH/CRITICAL source-resolvable gap hidden as a design assumption
```

Statuses:

- DD_READY_FOR_VERIFICATION
- DD_BLOCKED_SOURCE_GAP
- DD_BLOCKED_DEPENDENCY

## Output

Use the active workflow-declared DD output path under the current run root.
