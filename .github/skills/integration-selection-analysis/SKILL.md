---
name: integration-selection-analysis
description: Determine exactly how concrete clients/adapters/protocols/backends are selected, with mandatory counterexample search and promotion gates before routing rules enter canonical decision matrices.
license: MIT
---

# Integration Selection Analysis — V2

## Core Question

Under exactly what conditions is each concrete implementation selected?

## Search

Find:
- abstractions
- all implementations
- factories/providers/registries
- DI/container wiring
- config
- enums/constants
- target/model/version branches
- operation-specific routing
- fallback paths

## Separate Dimensions

Do not merge:
1. operation selection
2. target/entity selection
3. mode selection
4. concrete implementation selection
5. protocol/transport selection
6. fallback selection

## Candidate Rule

Every routing rule begins as candidate.

Example candidate:

```text
For operation X and target Y, condition Z selects Client A.
```

## Promotion Gate for Routing

Before adding a row to `00_master_decision_matrix.md`:

- trace caller to selector
- identify concrete implementation
- verify active wiring
- search all relevant branches
- search alternate implementations
- inspect config-driven behavior
- inspect fallback
- scope the rule narrowly
- assign Evidence ID
- mark Promotion Status=PROMOTED

If any condition is unresolved, keep it in `00_hypotheses.md`, not canonical matrix.

## Output

`docs/reverse-engineering/integration-selection.md`

Update:
- evidence ledger
- hypotheses/open questions
- canonical matrix only for promoted rows
