---
name: runtime-flow-analysis
description: Trace a runtime operation end-to-end, record candidate claims, verify important behavior, and promote only claims that pass source verification, counterexample search, and scope checks.
license: MIT
---

# Runtime Flow Analysis — V2

## Start

Read canonical memory:

- `00_current_understanding.md`
- `00_evidence_ledger.md`
- `00_master_decision_matrix.md`

Read `00_hypotheses.md` and `00_open_questions.md` only if relevant.

## Trace

Generic target:

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
8. decide:
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
