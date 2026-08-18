---
name: reverse-engineering-bootstrap
description: Initialize V3.0 repository-backed reverse-engineering memory, workflow state, investigation coverage, baseline identity, and broad candidate reconnaissance without prematurely promoting architecture claims.
license: MIT
---

# Reverse Engineering Bootstrap — V3.0

## Goal

Create the persistent workspace and broad investigation map before deep tracing.

## Create / Ensure

Under `docs/reverse-engineering/`:

```text
00_current_understanding.md
00_evidence_ledger.md
00_master_decision_matrix.md
00_hypotheses.md
00_open_questions.md
00_workflow_state.md
00_investigation_coverage.md
```

## Baseline Identity

Record repository, branch, HEAD commit, and relevant build/module identity when available.

## Broad Reconnaissance

Identify candidate locations for:

- inbound interfaces
- startup/bootstrap
- service/business logic
- integrations/adapters/gateways
- selectors/factories/providers/registries/DI
- configuration sources/loaders/defaults
- persistence/DAO/ORM/schema/migrations
- external boundaries
- error/retry/fallback
- lifecycle/concurrency
- security/auth
- observability/audit
- tests
- architecture docs

Do not infer active behavior from names alone.

## Investigation Coverage

Initialize a matrix:

| Domain | Applicable? | Candidate Source Areas | Depth | High-Impact Gap? | Notes |
|---|---|---|---|---|---|

Depth values:

```text
NOT_APPLICABLE
DISCOVERED
TRACED
VERIFIED
GAP_HIGH
GAP_MEDIUM
GAP_LOW
EXTERNALLY_BLOCKED
```

## Open Question Schema

Use:

| Q-ID | Question | Impact | Closure State | Search Performed | Evidence Needed | External Dependency | Next Action |
|---|---|---|---|---|---|---|---|

Impact:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

Closure state:

```text
SOURCE_SEARCH_PENDING
SOURCE_SEARCH_IN_PROGRESS
SOURCE_EXHAUSTED
EXTERNALLY_BLOCKED
RESOLVED_VERIFIED
RESOLVED_REJECTED
NOT_APPLICABLE
```

## Candidate Findings

- write candidates to `00_hypotheses.md`
- unresolved questions to `00_open_questions.md`
- candidate evidence rows to `00_evidence_ledger.md`
- keep canonical baseline empty/minimal until promotion

## Stop Condition

Stop after workspace, broad topology, coverage map, candidate claims, and prioritized investigation questions exist.

Bootstrap is reconnaissance, not full-system understanding.
