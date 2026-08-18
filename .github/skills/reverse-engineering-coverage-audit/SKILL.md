---
name: reverse-engineering-coverage-audit
description: Audit reverse-engineering completeness by finding important architectural domains, entry points, implementations, configuration paths, boundaries, persistence areas, or lifecycle behaviors that were never investigated deeply enough.
license: MIT
---

# Reverse Engineering Coverage Audit

## Mission

Challenge completeness, not just correctness.

Ask:

```text
What important architecture did the previous investigation fail to look at?
```

## Inputs

Review compactly:

```text
00_investigation_coverage.md
00_current_understanding.md
00_master_decision_matrix.md
00_open_questions.md
00_evidence_ledger.md
```

Compare against current repository topology and source search.

## Coverage Domains

Assess applicability and depth for:

- inbound surfaces
- startup/bootstrap
- major business/service modules
- representative runtime flows
- all materially distinct integration implementations
- factories/providers/registries/DI
- configuration sources/defaults/precedence
- external boundaries
- persistence/schema
- error/retry/fallback
- lifecycle/concurrency
- auth/security
- observability/audit
- compatibility/version/model branches
- background/internal jobs
- tests revealing alternate behavior

## Adversarial Coverage Search

Search for source clusters that are absent from the baseline:

- implementations never referenced by decision matrix
- config keys never traced to consumers
- DB/DAO/schema packages not represented
- process/HTTP/socket clients not represented
- entry points not represented
- factories/providers without verified routing claims
- background workers not represented
- model/version switches not represented

## Coverage Matrix

| Domain | Source Evidence It Exists | Existing RE Coverage | Depth | Gap | Impact | Required Follow-up |
|---|---|---|---|---|---|---|

Depth:

```text
NOT_APPLICABLE
DISCOVERED
TRACED
VERIFIED
```

Gap impact:

```text
CRITICAL
HIGH
MEDIUM
LOW
NONE
```

## Gate

Any CRITICAL/HIGH source-resolvable coverage gap means baseline readiness is:

```text
NOT_READY_HIGH_IMPACT_GAPS
```

Create/open a question and return it to `/resolve-high-impact-unknowns`.

## Output

Create:

```text
docs/reverse-engineering/11_reverse_engineering_coverage_audit.md
```

Update `00_investigation_coverage.md` and `00_workflow_state.md`.
