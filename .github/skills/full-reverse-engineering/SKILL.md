---
name: full-reverse-engineering
description: Orchestrate V3.0 deep source-first reverse engineering, evidence hardening, runtime/config/persistence tracing, high-impact unknown closure, coverage audit, promotion gates, adversarial verification, and readiness certification.
license: MIT
---

# Full Reverse Engineering Orchestrator — V3.0

## Mission

Build a deep, source-backed system baseline that is useful for high-impact work.

V3 deliberately separates:

```text
A. AGGRESSIVE DISCOVERY
B. EVIDENCE HARDENING
C. HIGH-IMPACT GAP CLOSURE
D. READINESS CERTIFICATION
```

Do not optimize for producing many verified claims.
Optimize for reconstructing the important architecture and closing material gaps.

## Canonical Workspace

Maintain:

```text
docs/reverse-engineering/00_current_understanding.md
docs/reverse-engineering/00_evidence_ledger.md
docs/reverse-engineering/00_master_decision_matrix.md
docs/reverse-engineering/00_hypotheses.md
docs/reverse-engineering/00_open_questions.md
docs/reverse-engineering/00_workflow_state.md
docs/reverse-engineering/00_investigation_coverage.md
```

## Persistent Workflow State

`00_workflow_state.md` MUST contain:

- repository / branch / baseline commit
- current phase
- completed phases
- pending investigations
- HIGH/CRITICAL unknowns and their closure state
- baseline readiness status
- exact resume instruction

## Phase 0 — Bootstrap and Topology Reconnaissance

Run `/reverse-engineering-bootstrap`.

Additionally create/update `00_investigation_coverage.md` with architecture domains and initial applicability.

Perform broad source reconnaissance before narrowing.

Do not promote from filenames/package names alone.

## Phase 1 — Inbound and Startup Surface

Identify:

- REST/HTTP/RPC/CLI/event/job/batch entry points
- application startup/bootstrap
- dependency/container initialization
- major registries/providers
- scheduler/background workers

Create:

```text
docs/reverse-engineering/01_inbound_surface.md
```

Include a concise Mermaid component/flow map when source supports it.

## Phase 2 — Representative Runtime Flows

Run `/runtime-flow-analysis` for enough representative operations to cover materially different architecture paths.

Do not blindly cap at 3–5 flows if additional flows represent distinct routing/boundary mechanisms.

Prefer a coverage-driven set:

- major read path
- major write/mutating path
- authentication/session path if present
- one path per materially different integration/backend
- background/internal path if architecturally distinct

Create/update:

```text
docs/reverse-engineering/02_representative_runtime_flows.md
```

Include source-backed Mermaid flows for important paths.

## Phase 3 — Integration Selection and Runtime Binding

Run:

```text
/integration-selection-analysis
/runtime-binding-verification
```

Prove how abstractions become concrete implementations.

Trace:

```text
caller
→ selector/factory/provider/DI
→ configuration/runtime state
→ concrete implementation
→ boundary
```

Create/update:

```text
docs/reverse-engineering/03_integration_selection.md
docs/reverse-engineering/03_runtime_binding.md
```

Do not leave a HIGH-impact routing claim at enum/class-name level.

## Phase 4 — Configuration Source and Precedence

Run `/configuration-source-trace` for configuration that materially changes behavior, especially routing, protocol, feature enablement, target/model/version behavior, authentication, retry, or external endpoints.

Trace each important setting through:

```text
external source
→ loader/parser
→ key/default
→ override precedence
→ runtime object/state
→ consumer/branch
→ behavioral effect
```

Create:

```text
docs/reverse-engineering/04_configuration_and_modes.md
```

If a value originates outside the repo, prove the code-side injection point and classify only the unavailable value as external.

## Phase 5 — External Boundaries

Identify real boundaries:

- HTTP/API
- command/process
- socket
- SDK/native
- DB
- broker
- filesystem
- RPC/cloud service
- repository-specific external mechanisms

For each important boundary capture:

- caller
- concrete adapter/client
- request/command construction
- endpoint/target source
- authentication/security where visible
- response/result parsing
- timeout/retry/fallback
- error mapping

Create:

```text
docs/reverse-engineering/05_boundaries.md
```

## Phase 6 — Persistence and Data Model

Determine whether persistence exists and is material.

If applicable, run `/persistence-schema-reverse-engineering`.

Trace:

```text
business/service
→ repository/DAO/query layer
→ ORM/SQL/schema definition
→ tables/entities/keys/relationships
→ read/write lifecycle
```

Search migrations, DDL, schema bootstrap, ORM mappings, embedded SQL, test schemas, upgrade scripts, and generated schema artifacts.

Create:

```text
docs/reverse-engineering/06_persistence_and_data.md
```

If persistence/schema is not applicable, record `NOT_APPLICABLE` with evidence.
If schema is external, distinguish code-known schema facts from externally unavailable details.

## Phase 7 — Error, Retry, Fallback, Lifecycle, Concurrency

Trace important failure and lifecycle behavior:

- validation errors
- routing/config errors
- connection/downstream failures
- timeout
- parsing/mapping errors
- retry/reconnect/fallback
- resource creation/disposal
- pooling/session/cache lifecycle
- thread/executor/async behavior when material

Create:

```text
docs/reverse-engineering/07_error_retry_fallback_lifecycle.md
```

## Phase 8 — Claim Verification and Promotion

Run `/claim-verification-and-promotion` on HIGH-impact candidates first.

Promote only claims that pass V3 verification rules.

Update:

```text
00_current_understanding.md
00_master_decision_matrix.md
00_evidence_ledger.md
00_hypotheses.md
```

## Phase 9 — High-Impact Unknown Closure

MANDATORY before readiness certification.

Run:

```text
/resolve-high-impact-unknowns
```

For every HIGH or CRITICAL unknown:

1. determine whether current source/runtime/config/tests can answer it
2. dispatch to targeted tracing skill(s)
3. search until resolved or evidence-backed exhaustion is reached
4. update claim/open-question state
5. verify/promote resolved facts where appropriate

A HIGH/CRITICAL item may remain only as:

```text
EXTERNALLY_BLOCKED
NOT_APPLICABLE
```

or the baseline is NOT ready.

## Phase 10 — Adversarial Baseline Audit

Run `/adversarial-baseline-audit`.

Attack high-impact promoted claims and recently resolved unknowns.

Explicitly challenge:

- runtime binding
- configuration provenance
- routing rules
- persistence/schema assumptions
- fallback/legacy paths
- over-generalized flow claims

Downgrade/supersede failures with preserved history.

## Phase 11 — Coverage Audit

Run `/reverse-engineering-coverage-audit`.

Ask not only "are claims verified?" but:

```text
what important system areas did we fail to investigate?
```

Any newly detected HIGH/CRITICAL gap returns the workflow to Phase 9.

Repeat Phase 9–11 until no source-resolvable HIGH/CRITICAL gap remains or workflow must stop as PARTIAL_RESUMABLE.

## Phase 12 — Final Baseline Consolidation

Create:

```text
docs/reverse-engineering/12_final_reverse_engineered_baseline.md
```

Include:

1. system purpose and scope
2. baseline identity
3. architecture/component overview
4. inbound/startup architecture
5. representative runtime flows
6. integration selection/runtime binding
7. configuration source/precedence
8. external boundaries
9. persistence/data model where applicable
10. error/retry/fallback
11. lifecycle/concurrency where material
12. canonical routing/decision summary
13. promoted evidence index
14. rejected/superseded corrections
15. investigation coverage summary
16. remaining external blockers
17. readiness status

Use Mermaid diagrams for the important static and runtime views when source supports them.

## Unknown Closure States

Every unresolved question must use one:

```text
SOURCE_SEARCH_PENDING
SOURCE_SEARCH_IN_PROGRESS
SOURCE_EXHAUSTED
EXTERNALLY_BLOCKED
RESOLVED_VERIFIED
RESOLVED_REJECTED
NOT_APPLICABLE
```

No vague HIGH-impact `UNKNOWN` is allowed at completion.

## Readiness Gate

### BASELINE_READY

Allowed only when:

```text
unresolved CRITICAL source-resolvable unknowns = 0
AND
unresolved HIGH source-resolvable unknowns = 0
AND
coverage audit has no HIGH/CRITICAL uninvestigated domain
AND
adversarial audit has no unresolved HIGH/CRITICAL contradiction
```

### BASELINE_READY_WITH_EXTERNAL_BLOCKERS

Allowed only when all remaining HIGH/CRITICAL items are proven `EXTERNALLY_BLOCKED`, with:

- repository search coverage
- code-side injection/boundary point where applicable
- exact external evidence required to close them

### NOT_READY_HIGH_IMPACT_GAPS

Use when HIGH/CRITICAL source-resolvable investigation remains.

### PARTIAL_RESUMABLE

Use when context/tool/time limits interrupt the workflow.
Persist exact next investigation and resume command.

## Context Budget

Do not repeatedly load the whole baseline or repository.

For each phase:

```text
00_workflow_state
+ compact canonical baseline
+ current phase artifact
+ targeted source
+ relevant open questions
```

Persist detailed results to files.

## Final Console Response

Do not print the full baseline.

Return only:

```text
Reverse-engineering status: <readiness status>
Baseline commit: <commit>
Promoted high-impact claims: <count>
Rejected/superseded claims: <count>
High-impact source-resolvable unknowns: <count>
External blockers: <count>
Coverage gaps: <count>
Key artifacts: <paths>
Next action: <exact command or NONE>
```

Never say "ready for high-impact work" when status is `NOT_READY_HIGH_IMPACT_GAPS` or `PARTIAL_RESUMABLE`.
