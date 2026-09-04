---
name: claim-verification-and-promotion
description: Verify candidate reverse-engineering claims against current source, actively search for counterexamples, narrow scope, and promote only defensible claims into canonical baseline memory.
---

# Claim Verification and Promotion — 4.0

## Mission

Take candidate claims from:
- `00_hypotheses.md`
- detailed reverse-engineering docs
- pending evidence rows

and determine whether they deserve canonical promotion.

## For Each Claim

### 1. Restate Precisely

Avoid words like:
- always
- all
- never
- global
- only

unless proven.

### 2. Supporting Evidence

Trace exact current source:
- caller
- condition
- selector
- implementation
- boundary
- config
as relevant.

Material source-backed claims must record a repo-relative source path. When a specific class/method/function/config key is involved, record the symbol/key as well. Line/range is preferred when practical.

Evidence precision hierarchy:

```text
path + symbol + line/range   preferred
path + symbol                strong
path                         minimum for material source-backed claim
class name only              insufficient when path is discoverable
```

### 3. Counterexample Search

Actively search:
- other implementations
- other call sites
- alternate branches
- config-driven paths
- target/model/version/mode variations
- fallback/retry
- reflection/service loader
- tests hinting at alternate production behavior

### 4. Scope Check

Narrow the claim to the actual proven domain.

For claims spanning multiple endpoints/operations/modes, create a compact scope matrix:

| Surface / Operation | Claim Applies? | Condition | Evidence |
|---|---:|---|---|

Do not transfer a condition from one surface to another without evidence.

### 4A. Field / Data Provenance Gate

Mandatory for claims about:

- response/output fields
- conditionally exposed data
- persisted/configured values
- messages/events
- identifiers/normalized values
- downstream-derived state

Prove:

```text
trigger / request condition
→ source/downstream retrieval
→ source field/data availability
→ parse/decode
→ transform/normalize
→ mapping/storage
→ serialization/output
→ observable result
```

Rules:

- conditional output may be implemented indirectly by conditional retrieval
- do not require an explicit output-layer condition if upstream flow already guarantees the result
- implementation shape alone is not enough to promote an observable-behavior claim
- if a material provenance link is missing, do not PROMOTE

### 5. Baseline Version

Record current commit/branch if available.

### 6. Decision

#### PROMOTE
Requirements satisfied, including provenance when applicable.

#### VERIFIED_NOT_PROMOTED
Evidence supports the claim but one promotion governance requirement is intentionally deferred.

#### KEEP AS HYPOTHESIS
Useful but incomplete.

#### REJECT
Contradicted or unsupported.

## Update Ledger

Record:
- verification method
- counterexample search
- result
- status
- supersession if applicable

## Canonical Promotion

Only PROMOTED claims may be copied into:
- `00_current_understanding.md`
- `00_master_decision_matrix.md`

Canonical entries must reference Evidence ID.

## Promotion Completion Gate

Before PROMOTE:

```text
[ ] claim wording is precise and scope-limited
[ ] current-source support exists
[ ] counterexamples/alternate paths were searched
[ ] scope conditions were not borrowed from another surface
[ ] runtime wiring is proven where relevant
[ ] field/data provenance is proven for observable-data claims
[ ] no material evidence link remains unresolved
[ ] material source evidence includes repo-relative path
[ ] symbol/config key is recorded where applicable
```

If an applicable item is unresolved, use `VERIFIED_NOT_PROMOTED`, `KEEP AS HYPOTHESIS`,
or another non-promoted state as appropriate.

## Challenge Reverification

A user correction or reviewer disagreement is not evidence.

When a promoted/candidate claim is challenged:

- reopen the claim
- re-trace current source
- search counterevidence
- revise only if evidence supports revision

## Important

A claim becoming familiar through repetition is not evidence.
