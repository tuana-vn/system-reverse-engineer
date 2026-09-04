---
name: baseline-source-of-truth-maintenance
description: Safely maintain canonical reverse-engineering baseline after verified current-source changes. Enforces evidence lifecycle, promotion gates, supersession history, and removal of stale claims.
---

# Baseline Source-of-Truth Maintenance — 4.0

## Preconditions

Proceed only if:
- user states change is merged/current, or
- checked-out source proves change exists, or
- user explicitly requests rebaseline against current source.

## Do Not Trust Existing Baseline Blindly

Re-verify high-impact affected claims.

## Update Process

1. determine current branch/commit
2. identify affected promoted claims
3. verify current source
4. search counterexamples
5. create new evidence rows
6. mark old evidence SUPERSEDED when appropriate
7. promote new claims
8. update canonical understanding/matrix
9. update hypotheses/open questions
10. preserve evidence history

## Canonical Rule

Only PROMOTED VERIFIED claims enter:
- `00_current_understanding.md`
- `00_master_decision_matrix.md`

## Evidence History

Never delete contradictory history without trace.

Use:
`E-0042 SUPERSEDED BY E-0198`.

## Final Check

Every canonical claim must:
- reference Evidence ID
- match current source scope
- have promotion status PROMOTED


## Consumer Baseline Maintenance

When a verified change affects architecture, runtime flow, integration selection, configuration behavior, state ownership, or lifecycle:

- update the relevant model artifact;
- update the affected Mermaid diagram when relationships changed;
- update `CURRENT_STATE_TDD.md`;
- keep the readiness/adversarial audit separate from the TDD.

Do not leave canonical evidence updated while the consumer-facing architecture model remains stale.
