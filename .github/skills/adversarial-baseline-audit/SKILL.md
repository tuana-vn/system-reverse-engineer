---
name: adversarial-baseline-audit
description: Challenge promoted reverse-engineering baseline claims by trying to disprove them, detect over-generalization, stale evidence, test-as-runtime mistakes, and persistent hallucination before high-impact migration or design work.
---

# Adversarial Baseline Audit — 4.0

## Mission

Assume the canonical baseline may contain mistakes.

Do not try to confirm it.
Try to break it.

## Input

Review:
- `00_current_understanding.md`
- `00_evidence_ledger.md`
- `00_master_decision_matrix.md`

Select high-impact PROMOTED claims.

Prioritize:
- routing/client selection
- protocol/external boundary
- business behavior
- compatibility/error rules
- externally observable field/data behavior
- claims used by migration/design
- claims reused by patch/compliance/test-design work

## Attack Each Claim

Ask:

1. Is scope broader than evidence?
2. Was a condition proven for one endpoint/operation generalized to another?
3. Is evidence stale against current commit?
4. Was a test mistaken for production wiring?
5. Are there alternate implementations or alternate caller paths?
6. Are there hidden config branches?
7. Is fallback missing?
8. Does a different operation behave differently?
9. Does target/model/version/mode change behavior?
10. Is there an inactive/legacy path confused with active?
11. Does current source contradict the memory statement?
12. For an externally observable field/data claim, was full provenance actually proven?
13. Could the claimed conditional output be implemented earlier by conditional retrieval/mapping?
14. Was one representative external entry point mistaken for complete exposure?
15. If a no-impact claim exists, were all source-visible invocation sites closed?


## Mandatory Attack Dimensions

### Scope Leakage Attack

For claims that mention conditions, modes, parameters, or endpoint-specific behavior:

- reconstruct a compact scope matrix
- verify the condition independently per surface/operation
- search for sibling operations that share code but have different requirements
- downgrade any claim whose wording is broader than the proven scope

### Field / Data Provenance Attack

For claims about output fields, persisted values, messages, identifiers, or conditional data:

```text
trigger
→ retrieval/source
→ parse/decode
→ transform/normalize
→ mapping/storage
→ serialization/output
→ observable result
```

Attack every link.

A missing explicit serializer/output condition is NOT evidence of a gap if earlier
conditional retrieval or mapping already guarantees the behavior.

### Boundary → Exposure Closure Attack

For claims that a downstream boundary is or is not externally reachable:

```text
impacted / important boundary
← every invocation/construction site
← every caller chain
← every external entry point or proven internal root
```

Do not accept:
- one representative REST endpoint as complete exposure
- `NO_DIRECT_*_IMPACT` while an invocation site remains unresolved
- a downstream CLI integration being mislabeled as the product's own CLI entry point

### Premature Verdict Attack

Attack claims that appear to have been promoted before:
- full runtime/control-flow trace
- field/data provenance where applicable
- alternate-path search
- exposure closure where applicable
- current-source reverification

## Audit Matrix

| Evidence ID | Promoted Claim | Scope Attack | Provenance Attack | Exposure Attack | Counterevidence | Verdict | Action |
|---|---|---|---|---|---|---|---|

Verdict:
- HOLDS
- OVER-GENERALIZED
- PROVENANCE_INCOMPLETE
- EXPOSURE_INCOMPLETE
- STALE
- CONTRADICTED
- INSUFFICIENTLY_VERIFIED
- UNKNOWN

## Action

Do not silently rewrite.

If contradicted:
- mark evidence REJECTED or SUPERSEDED
- remove canonical claim only with explicit evidence note
- preserve history in ledger
- add corrected candidate claim
- require re-promotion

## Completion Gate

Before declaring a high-impact promoted claim `HOLDS`:

```text
[ ] claim scope matches evidence scope
[ ] current source still supports the claim
[ ] alternate implementations/caller paths were searched
[ ] field/data provenance is complete when the claim is data/output-related
[ ] boundary/exposure closure is complete when reachability is claimed
[ ] no sibling operation contradicts the generalized rule
[ ] tests were not substituted for production wiring
```

If an applicable item is unresolved, do not use `HOLDS`.

## Output

`docs/reverse-engineering/audits/<date-or-baseline>-adversarial-audit.md`
