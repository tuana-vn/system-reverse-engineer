---
name: adversarial-baseline-audit
description: Challenge promoted reverse-engineering baseline claims by trying to disprove them, detect over-generalization, stale evidence, test-as-runtime mistakes, and persistent hallucination before high-impact migration or design work.
license: MIT
---

# Adversarial Baseline Audit

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
- claims used by migration/design

## Attack Each Claim

Ask:

1. Is scope broader than evidence?
2. Is evidence stale against current commit?
3. Was a test mistaken for production wiring?
4. Are there alternate implementations?
5. Are there hidden config branches?
6. Is fallback missing?
7. Does a different operation behave differently?
8. Does target/model/version/mode change behavior?
9. Is there an inactive/legacy path confused with active?
10. Does current source contradict the memory statement?

## Audit Matrix

| Evidence ID | Promoted Claim | Attack Performed | Contradictory Evidence | Verdict | Action |
|---|---|---|---|---|---|

Verdict:
- HOLDS
- OVER-GENERALIZED
- STALE
- CONTRADICTED
- INSUFFICIENTLY VERIFIED
- UNKNOWN

## Action

Do not silently rewrite.

If contradicted:
- mark evidence REJECTED or SUPERSEDED
- remove canonical claim only with explicit evidence note
- preserve history in ledger
- add corrected candidate claim
- require re-promotion

## Output

`docs/reverse-engineering/audits/<date-or-baseline>-adversarial-audit.md`
