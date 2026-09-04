---
name: reverse-engineering-coverage-audit
description: Audit reverse-engineering completeness by finding important architectural domains, entry points, implementations, configuration paths, boundaries, persistence areas, or lifecycle behaviors that were never investigated deeply enough.
---

# Reverse Engineering Coverage Audit — 4.0

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
- boundary → exposure closure for important downstream operations
- field/data provenance for externally meaningful values
- request/input semantics for externally visible interfaces
- persistence/schema
- error/retry/fallback
- lifecycle/concurrency
- auth/security
- observability/audit
- compatibility/version/model branches
- background/internal jobs
- tests revealing alternate behavior

## Adversarial Coverage Search

Search for source clusters and evidence chains absent from the baseline:

- implementations never referenced by decision matrix
- config keys never traced to consumers
- DB/DAO/schema packages not represented
- process/HTTP/socket/CLI clients not represented
- entry points not represented
- downstream boundaries with unresolved invocation sites
- shared runtime methods with only one external caller documented
- response/output fields with no provenance chain
- conditional output claims with no retrieval/mapping evidence
- factories/providers without verified routing claims
- background workers not represented
- model/version switches not represented
- endpoint-specific conditions generalized across sibling operations


## Required Cross-Cutting Coverage Checks

In addition to architecture domains, audit these evidence dimensions:

### A. Exposure Closure Coverage

For important downstream boundaries, ask:

```text
boundary
← all direct invocation sites
← all caller chains
← all external entry points / proven internal roots
```

Coverage is incomplete when:
- one invocation site is unresolved
- only a representative external endpoint is documented
- a no-impact claim lacks a terminating reverse trace

### B. Field / Data Provenance Coverage

For externally meaningful fields/data, ask whether baseline artifacts prove:

```text
trigger
→ retrieval/source
→ parse
→ transform
→ mapping/state
→ serialization/output
→ observable result
```

Coverage is incomplete if a promoted behavior claim skips a material link.

### C. Scope-Isolation Coverage

Check whether endpoint/operation-specific conditions are recorded independently.
Shared implementation does not prove shared contract semantics.

## Coverage Matrix

| Domain / Evidence Dimension | Source Evidence It Exists | Existing RE Coverage | Depth | Gap | Impact | Required Follow-up |
|---|---|---|---|---|---|---|

Depth:

```text
NOT_APPLICABLE
DISCOVERED
TRACED
PROVENANCE_TRACED
EXPOSURE_CLOSED
VERIFIED
```

Use only states applicable to the domain; do not force provenance/exposure states where irrelevant.

Gap impact:

```text
CRITICAL
HIGH
MEDIUM
LOW
NONE
```

## Consumer-Model Coverage

Also audit whether the verified evidence has been converted into a usable system model. Check:

```text
5 mandatory diagram artifacts present
major subsystem responsibilities modeled
primary runtime flows modeled
known external integrations modeled
behavior-changing configuration selectors modeled
persistence/state ownership modeled
diagram nodes/edges evidence-linked
CURRENT_STATE_TDD references the model artifacts
```

A baseline with complete evidence tables but missing architecture synthesis is not complete.

## Gate

Any CRITICAL/HIGH source-resolvable coverage gap or mandatory consumer-model gap means baseline readiness is:

```text
NOT_READY_HIGH_IMPACT_GAPS
```

Create/open a question and return it to `/resolve-high-impact-unknowns`.

Treat unresolved provenance or exposure closure as HIGH/CRITICAL when it can change:
- externally observable behavior
- API/entry-point impact scope
- routing/integration conclusions
- compatibility or migration decisions.

## Output

Create:

```text
docs/reverse-engineering/11_reverse_engineering_coverage_audit.md
```

Update `00_investigation_coverage.md` and `00_workflow_state.md`.
