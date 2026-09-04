---
name: regression-test-design
description: Generate a focused evidence-based regression test matrix from verified requirements, runtime behavior, patches, impact reviews, or proposed designs. Isolate requirement scope, derive provenance-aware test oracles, and avoid combinatorial explosion.
---

# Regression Test Design — 4.0

## Evidence Order

Use the strongest available evidence:

1. explicit requirement/specification
2. current source
3. promoted verified baseline
4. verified patch-impact/compliance report
5. proposed design
6. patch/diff as candidate behavior
7. existing tests as evidence, not unquestioned truth

Do not invent expected behavior.

## 1. Canonical Scope

When a requirement exists, create:

| Rule | Surface / Operation | Applies? | Condition | Expected Observable Behavior |
|---|---|---:|---|---|

Rules:

- evaluate each row independently
- do not transfer conditions between endpoints/surfaces
- preserve exclusions/non-applicable operations
- unresolved scope remains `SCOPE_UNRESOLVED`

## 2. Derive Tests From

- business rules
- branch conditions
- routing decisions
- target/model/mode combinations
- integrations
- success/failure
- timeout/retry/fallback
- compatibility paths
- input/parameter semantics
- field/data provenance
- audit/observability where behaviorally relevant

For input-driven behavior, distinguish:

- valid supported input
- unsupported input name
- wrong-case input name
- invalid supported value
- invalid supported-input combination
- omitted/null/empty/default

## 3. Provenance-Aware Test Oracle

For tests involving changed output/data/state, prove:

```text
requirement / verified rule
→ trigger/input condition
→ expected downstream/source data availability
→ expected transform/mapping/state
→ expected serialization/output
→ observable result
```

Conditional output may be achieved indirectly by conditional retrieval.
Do not demand an explicit output-layer condition when upstream flow already guarantees the result.

If the oracle cannot be proven, use:

`EXPECTED_BEHAVIOR_UNRESOLVED`

and identify the missing evidence.

## 4. Prioritize

Prefer:

1. changed externally observable rules
2. changed branches
3. high-risk shared paths
4. boundary conditions
5. failure translation
6. preserved behavior outside change scope
7. performance-sensitive unchanged paths when the patch changes retrieval/call cost

Avoid blindly multiplying every dimension.

Use equivalence classes, boundaries, decision tables, and pairwise/risk-based combinations.

## 5. Test Matrix

| Test ID | Level | Rule / Flow / Risk | Surface / Operation | Preconditions | Input | Expected Route / Downstream Interaction | Expected Data Provenance / State | Expected Observable Result | Regression Purpose | Evidence | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|

Levels:

- UNIT
- COMPONENT
- API_CONTRACT
- INTEGRATION
- END_TO_END
- REGRESSION

An externally visible change must not be covered only by unit tests.

Group scenarios as applicable:

- Positive
- Negative
- Compatibility
- Integration
- Data/State
- Regression
- Concurrency only if the changed path involves it

## 6. Coverage Gate

Before completion:

```text
[ ] requirement/scope isolation completed when applicable
[ ] expected results have evidence-backed oracles
[ ] changed output/data has provenance-aware expectations
[ ] unchanged behavior outside change scope has regression coverage
[ ] unsupported/wrong-case/invalid-value/invalid-combination inputs are not conflated
[ ] externally visible rules have contract/integration-level coverage where feasible
[ ] high-risk changed branches map to concrete tests
[ ] unresolved oracles are explicitly marked, not guessed
```

## Output

`docs/reverse-engineering/tests/<scope>-test-matrix.md`
