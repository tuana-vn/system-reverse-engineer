---
name: detailed-design-verification
description: Independently verify one artifact detailed design against current source, verified TDD, artifact registry, requirement/gap traceability, provenance/exposure evidence, dependencies, compatibility constraints, and implementability. Use before marking a design artifact implementation-ready.
license: MIT
---

# Detailed Design Verification

## Mission

Verify one detailed-design artifact independently.

Do not merely check internal consistency of the document.

```text
Requirement
→ Gap
→ Verified TDD
→ Registry Artifact
→ Detailed Design
↕
Current Source / Runtime Evidence
```

## 1. Traceability Verification

Verify:

| Check | Expected |
|---|---|
| Artifact ID | exists in registry |
| Requirement IDs | match registry/TDD |
| Gap IDs | verified gaps only |
| TDD Decision IDs | verified decisions |
| Existing anchors | exist and have claimed role |
| Proposed items | explicitly proposed |

## 2. Source / Runtime Verification

Check:

- caller/callee assumptions
- ownership/lifecycle
- configuration/binding
- data/state source
- result/error semantics
- integration boundaries
- all material exposure paths
- field/data provenance
- sibling operations/counterexamples

Do not approve a design because the signatures "look plausible".

## 3. Design Drift Verification

Detect:

- new behavior not approved by TDD
- missing TDD behavior
- changed requirement scope
- added validation/defaults
- omitted MUST-NOT / non-goal behavior
- invented shared abstraction
- unnecessary restructuring
- hidden migration/compatibility effects


## 3A. Architecture State Separation Gate

This gate is mandatory whenever the DD contains architecture/component/relationship diagrams or
architecture prose.

Independently enumerate every architecture view and classify every material node/relationship as:

```text
CURRENT
PROPOSED
UNKNOWN
```

Do not trust the section title.

Required checks:

| Check | Required |
|---|---:|
| Every CURRENT node exists in current source/evidence | 100% |
| Every CURRENT relationship is source/evidence-backed | 100% |
| PROPOSED nodes shown in a CURRENT-only view | 0 |
| PROPOSED relationships shown as CURRENT | 0 |
| UNKNOWN items promoted to CURRENT | 0 |
| Diagram title/state labels/prose agree | 100% |

If a section labeled CURRENT contains a PROPOSED component or relationship as though it already
exists, record:

`CURRENT_PROPOSED_ARCHITECTURE_CONTAMINATION`

Routing:

- if the TDD remains valid and the defect is in DD representation/state labeling:
  `DD_PARTIALLY_VERIFIED`
- if the DD asserts materially false CURRENT behavior contradicted by source:
  `DD_CONTRADICTED_BY_SOURCE`
- if source cannot resolve the classification:
  `DD_BLOCKED_SOURCE_GAP`

`DD_VERIFIED` is forbidden while any such finding remains.

## 3B. Quantified Risk / Confidence Claim Gate

Do not certify subjective labels by repetition.

Claims such as:

```text
Regression Risk: NONE
Risk: LOW
Confidence: HIGH
```

must have explicit measurable criteria and supporting closure evidence.

`Regression Risk: NONE` requires evidence that all materially affected compatibility/exposure paths
were enumerated and no regression mechanism remains in the verified scope.

For constructor/signature/lifecycle changes, verify all material construction/wiring sites before
accepting a zero-risk claim.

If a qualitative/zero-risk claim lacks measurable definition or evidence, record:

`UNSUPPORTED_QUALITATIVE_RISK_CLAIM`

and do not return `DD_VERIFIED` until the claim is removed, made evidence-backed, or expressed as an
explicit unresolved risk.


## 4. Implementability Verification

The design must be concrete enough that implementation tasks can be derived without guessing.

Check:

- exact existing source anchors
- proposed new artifact names/locations where needed
- interfaces/contracts
- branch/flow behavior
- data model/config changes
- dependency ordering
- error/failure semantics
- verification expectations

If implementers would need to invent a material design decision:

`DD_INCOMPLETE_IMPLEMENTATION_DETAIL`

## 5. Adversarial Counterexample Search

Before approval:

- search alternate callers
- search alternate implementations
- search model/version/config branches
- search earlier conditional retrieval/mapping
- search error/fallback paths
- search tests contradicting the design

## 6. Verdict Matrix

| DD Claim / Decision | Source/TDD Evidence | Counterevidence | Verdict | Required Correction |
|---|---|---|---|---|

Verdicts:

- VERIFIED
- PARTIALLY_VERIFIED
- CONTRADICTED
- SOURCE_NOT_RESOLVED
- OUT_OF_TDD_SCOPE

## 7. Gate

Overall:

- DD_VERIFIED
- DD_PARTIALLY_VERIFIED
- DD_CONTRADICTED_BY_SOURCE
- DD_BLOCKED_SOURCE_GAP

Only `DD_VERIFIED` may advance to WBS generation.

Update the design artifact registry status accordingly.

## Output

Use the active workflow-declared DD verification output path under the current run root.
