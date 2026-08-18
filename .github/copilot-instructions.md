# Copilot Instructions — Evidence-Backed Reverse Engineering (V3.0)

## Purpose

This repository is analyzed and evolved using source-first, evidence-backed reverse engineering.

Repository vocabulary, protocol names, subsystem labels, and legacy terminology are search hints only. Do not infer architecture from names. Prove architecture, protocol, runtime selection, configuration, and business behavior from source.

## Reverse-Engineering Workspace

```text
docs/reverse-engineering/
```

Canonical:

```text
00_current_understanding.md
00_evidence_ledger.md
00_master_decision_matrix.md
```

Operational/non-canonical:

```text
00_hypotheses.md
00_open_questions.md
00_workflow_state.md
00_investigation_coverage.md
```

Canonical memory contains only PROMOTED VERIFIED current-system claims.

## Discovery vs Certification

Use two modes:

```text
DISCOVER aggressively from source
→ build detailed candidate flows/models
→ then VERIFY / counterexample-search / scope / promote
```

Do not make discovery shallow merely to avoid uncertainty.
Do not promote discovery narratives merely because they are detailed.

## Baseline Is an Accelerator, Not a Prison

If a task needs detail absent from baseline, return to CURRENT SOURCE and trace it.

An old `UNKNOWN` is not proof that the source cannot answer the question.

## High-Impact Unknown Rule

HIGH/CRITICAL unknowns must be actively closed before declaring high-impact readiness.

Allowed closure states:

```text
SOURCE_SEARCH_PENDING
SOURCE_SEARCH_IN_PROGRESS
SOURCE_EXHAUSTED
EXTERNALLY_BLOCKED
RESOLVED_VERIFIED
RESOLVED_REJECTED
NOT_APPLICABLE
```

Do not label something `EXTERNALLY_BLOCKED` without documenting repository search coverage and the exact external evidence required.

## Readiness Status

Use only:

```text
BASELINE_READY
BASELINE_READY_WITH_EXTERNAL_BLOCKERS
NOT_READY_HIGH_IMPACT_GAPS
PARTIAL_RESUMABLE
```

Never say "ready for high-impact work" while source-resolvable HIGH/CRITICAL gaps remain.

## Current vs Proposed Behavior

Always distinguish:

- CURRENT VERIFIED BEHAVIOR
- PROPOSED / FUTURE BEHAVIOR
- PATCH-IMPLIED BEHAVIOR
- ASSUMPTION
- UNKNOWN

Never update canonical baseline from unmerged patches, requirements, proposals, incident hypotheses, or unverified AI interpretation.

## Production Source Safety

Unless explicitly asked to implement:

- do not modify production source
- do not refactor/rename
- do not change runtime configuration
- do not change external behavior

## Integration Caution

For every external integration or protocol boundary, prove the concrete client/adapter, configuration source, runtime binding, invocation mechanism, request construction, response parsing, retry/fallback, and error mapping.

Do not assume labels, mode names, enums, or configuration values directly determine the downstream implementation. Trace configuration source → runtime binding → selected implementation.

## Persistence

If database/persistence exists, trace repository/DAO → concrete binding → SQL/ORM → schema/migration evidence. Distinguish code-known schema facts from externally unavailable authoritative DDL/runtime state.

## Context Discipline

Prefer:

```text
task
+ workflow/readiness state
+ compact canonical baseline
+ current high-impact question
+ targeted source
```

Avoid repeatedly loading every generated artifact or the whole repository.

## Tests

Tests are supporting evidence. Tests alone do not prove active production wiring.

## Output Discipline

Write detailed findings to repository artifacts.
Console output should normally contain only:

- readiness/review status
- major verified findings
- HIGH/CRITICAL blockers
- artifact paths
- exact next action
