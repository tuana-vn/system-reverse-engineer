---
name: design-artifact-decomposition-verification
description: Independently verify design artifact decomposition against a verified TDD. Enumerate implementation-significant proposed units independently, compare them with registry ownership, detect missing/implicit/semantically unrelated ownership, and block DD progression when ownership closure is incomplete.
license: MIT
---

# Design Artifact Decomposition Verification

## Purpose

Generator != verifier.

Do not trust `ARTIFACT_REGISTRY_READY` merely because the decomposition stage emitted it.

Independently re-read:

- verified TDD
- TDD verification
- design artifact registry
- authoritative requirement / verified gap where needed

Then independently enumerate implementation-significant proposed units from the TDD.

## 1. Independent Proposed Unit Inventory

Create a fresh inventory without copying the registry's artifact list.

A unit is implementation-significant when it creates a distinct:

- class/interface/exception/data carrier/adapter/policy/config owner
- responsibility or contract
- failure behavior
- lifecycle/dependency boundary
- state/configuration ownership
- verification obligation

Create:

| Proposed Unit | Type | TDD Evidence | Why Implementation-Significant? |
|---|---|---|---|

Do not infer "all units covered" from the artifact count.

## 2. Registry Ownership Comparison

For every independently enumerated proposed unit, require exactly one registry ownership disposition:

```text
DEDICATED_ARTIFACT:<ART-ID>
or
SUBORDINATE_TO:<ART-ID>
```

Create:

| Proposed Unit | Registry Owner | Dedicated/Subordinate | Registry Responsibility | Explicitly Owned? | Semantic Match? | Verdict |
|---|---|---|---|---:|---:|---|

Rules:

- a JavaDoc mention, import, method signature, `throws`, `@see`, dependency, or nearby prose is not ownership
- an artifact cannot own a semantically unrelated unit merely because it references it
- self-referential labels such as `SUBORDINATE_TO:ART-005` for the same ART-005 are invalid ownership semantics unless the registry clearly identifies a separate subordinate proposed unit
- existing modified components are not "subordinate to themselves"; their artifact ownership type should describe the artifact itself, while subordinate proposed units must be separately named

## 3. Required Quantitative Gates

```text
independent proposed-unit inventory completed = YES
proposed-unit ownership coverage = 100%
semantic owner match = 100%
unowned implementation-significant units = 0
implicitly-owned units = 0
```

If any threshold fails:

`ARTIFACT_DECOMPOSITION_VERIFICATION_FAILED`

If source/TDD evidence is insufficient to determine ownership:

`ARTIFACT_DECOMPOSITION_VERIFICATION_BLOCKED`

Only when all thresholds pass:

`ARTIFACT_DECOMPOSITION_VERIFIED`

## 4. Output

Use the workflow-declared output path.
Do not invent or reuse a legacy artifact path.

<!-- workflow-status-contract:start -->
```yaml
emitted_statuses:
  - ARTIFACT_DECOMPOSITION_VERIFIED
  - ARTIFACT_DECOMPOSITION_VERIFICATION_FAILED
  - ARTIFACT_DECOMPOSITION_VERIFICATION_BLOCKED
```
<!-- workflow-status-contract:end -->
