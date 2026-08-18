---
name: claim-verification-and-promotion
description: Verify candidate reverse-engineering claims against current source, actively search for counterexamples, narrow scope, and promote only defensible claims into canonical baseline memory.
license: MIT
---

# Claim Verification and Promotion

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

### 5. Baseline Version

Record current commit/branch if available.

### 6. Decision

#### PROMOTE
Requirements satisfied.

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

## Important

A claim becoming familiar through repetition is not evidence.
