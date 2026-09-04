---
name: runtime-flow-analysis
description: Trace a runtime operation end-to-end, record candidate claims, verify important behavior, and promote only claims that pass source verification, counterexample search, and scope checks.
---

# Runtime Flow Analysis — 4.0

## Start

Read canonical memory:

- `00_current_understanding.md`
- `00_evidence_ledger.md`
- `00_master_decision_matrix.md`

Read `00_hypotheses.md` and `00_open_questions.md` only if relevant.

## Trace

Generic control-flow target:

```text
Inbound trigger
→ entry handler
→ validation/conversion
→ service/use-case
→ orchestration
→ abstraction
→ selector/factory/provider
→ concrete implementation
→ real boundary
→ result/error mapping
```

Trace data flow in parallel whenever a value influences an external result:

```text
input / trigger
→ source retrieval
→ source field/data
→ parse/decode
→ transform/normalize
→ mapping/state
→ serialization/output
→ observable result
```

Control flow and data provenance are separate evidence dimensions. Prove both when needed.

## Scope Isolation

When multiple endpoints/operations/modes reach shared code, record the exact scope of each branch.

Do not transfer a condition observed in one entry point to another entry point merely because they share a downstream method.

## Field / Data Provenance

For externally meaningful fields/data, record:

| Surface | Field/Data | Trigger/Condition | Retrieval | Source | Transform | Mapping/State | Output | Evidence |
|---|---|---|---|---|---|---|---|---|

A conditional external result may be implemented by conditional retrieval earlier in the flow.
Do not infer that the output layer itself must contain the condition.

## Record Candidates First

New non-trivial findings start as CANDIDATE.

Do not write directly to canonical baseline.

## For Each Candidate

1. define exact scope
2. locate supporting source
3. verify runtime wiring when relevant
4. identify concrete implementation
5. search for counterexamples
6. inspect alternate branches/configuration where relevant
7. assign Evidence ID
8. for output/data claims, prove provenance through to observable result
9. search for alternate entry points or earlier conditional retrieval that could contradict the claim
10. decide:
   - PROMOTE
   - KEEP AS HYPOTHESIS
   - REJECT
   - LEAVE UNKNOWN

## Output

Detailed flow:
`docs/reverse-engineering/flows/<operation>.md`

Canonical updates:
only PROMOTED VERIFIED facts.

Hypotheses:
write non-promoted findings to `00_hypotheses.md`.

## Completion Gate

A runtime-flow document is incomplete when an applicable item is unresolved without explanation:

```text
[ ] entry-point scope is explicit
[ ] callers and downstream effects are traced far enough to classify exposure
[ ] branch conditions are not generalized beyond proven scope
[ ] externally meaningful field/data provenance is traced when applicable
[ ] observable result/error mapping is proven
[ ] alternate paths/counterexamples were searched
[ ] unresolved links remain hypotheses/unknowns rather than promoted facts
```
