---
name: regression-test-design
description: Generate a focused evidence-based unit/integration/regression test matrix from architecture, requirements, patches, or proposed designs while avoiding combinatorial explosion.
license: MIT
---

# Regression Test Design

## Derive Tests From

- business rules
- branch conditions
- routing decisions
- target/model/mode combinations
- integrations
- success/failure
- timeout/retry/fallback
- compatibility paths
- audit/observability where relevant

## Prioritize

Prefer:

1. changed branches
2. high-risk shared paths
3. boundary conditions
4. failure translation
5. preserved behavior outside change scope

Avoid blindly multiplying every dimension.

## Matrix

| Test ID | Rule/Flow/Risk | Preconditions | Input | Expected Route/Implementation | Expected Result | Priority |
|---|---|---|---|---|---|---|

Group:

- Unit
- Integration
- System
- Negative
- Regression
- Concurrency if needed

## Output

`docs/reverse-engineering/tests/<scope>-test-matrix.md`
