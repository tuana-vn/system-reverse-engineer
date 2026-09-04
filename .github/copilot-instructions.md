## Normative Methodology Baseline

Before materially changing methodology, workflow semantics, design gates, or agent boundary, read `docs/METHODOLOGY_BASELINE.md`. It is normative and overrides historical examples. Normal bug-fix releases must preserve the agent purpose and `IMPLEMENTATION_READY` stop boundary.

# Copilot Instructions — Repository-Specific Rules (4.0)

## Purpose

This repository is analyzed and evolved using source-first, evidence-backed reverse engineering.

Repository vocabulary may include framework names, business-domain terms, protocol labels, service names, deployment modes, or legacy abbreviations. Treat names as search hints only. Prove architecture, protocol, runtime selection, configuration, and business behavior from source.


## Workflow / Prompt / Skill Separation

For high-impact work, distinguish:

```text
workflow = stage order + gates
prompt   = exact task/scope/output for the current stage
skill    = reusable methodology
source   = evidence
artifact = persistent result
```

If a workflow exists, do not collapse multiple stages into one answer.

Use `/run-engineering-workflow` and require the stage artifact's `WORKFLOW_GATE`.
A missing gate is not a pass.

For a multi-stage workflow running in Autopilot, an intermediate stage gate is a checkpoint,
not completion of the user's task. After persisting a valid non-terminal transition, continue
the next stage automatically. Do not emit `Task complete` while `workflow_state.yaml` still
has a non-terminal `active_step`. Finish only at a workflow terminal state, explicit
`stop_after_step`, or a genuine blocking/input-required condition.

Do not assume a generic skill knows the feature-specific requirement scope.
Read the referenced task prompt.

## Workflow Execution / Delegation

Workflow stages are **direct execution by default**.

If `execution.delegation_mode` is absent or equals `direct_only`:

- do not spawn a General-purpose agent or background sub-agent for the stage;
- execute source discovery, repository searches, shell inspection, artifact generation,
  and gate validation directly in the selected custom agent;
- do not wait/poll an idle worker;
- transition only after the declared artifact exists and its `WORKFLOW_GATE` is valid.

Only an explicit `delegation_mode: bounded` permits delegation. A bounded delegated attempt
that becomes idle or produces no declared artifact must be abandoned after the first
no-progress observation and the stage must continue by direct execution.


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

## Integration Analysis Caution

### REST / HTTP clients
Prove the concrete client, URL/config source, endpoint, method, authentication, request/response mapping, retry policy, runtime binding, and error translation.

### Message consumers / producers
For Kafka, AMQP, queue, or event-driven flows, prove topic/queue configuration, producer/consumer binding, serialization, acknowledgment semantics, retry/dead-letter behavior, and the actual runtime call path.

### Native C/C++ boundaries
For executables, shared libraries, FFI/JNI/PInvoke, sockets, or subprocess calls, prove symbol/process selection, configuration, ownership, lifecycle, error propagation, and the concrete runtime binding.

### Python workers / jobs
For FastAPI/Flask/Django services, Celery/RQ workers, scheduled jobs, or CLI entry points, trace configuration source → startup/registration → selected implementation → downstream integration.

### Domain labels
Do not assume a business label such as `order`, `inventory`, `promotion`, or `payment` identifies the owning component. Trace entry point → runtime binding → implementation → persistence/integration.

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

## Reverse-Engineering Consumer Quality

For a full baseline, do not confuse evidence bookkeeping with system understanding. Produce a consumer-facing current-system model.

Mandatory full-baseline outputs include `CURRENT_STATE_TDD.md`, five evidence-linked Mermaid diagram artifacts, and canonical component/runtime/integration/configuration/persistence-state models.

Use these priorities:

```text
model > inventory
relationships > file counts
behavior > component names
diagrams > repeated prose
consumer usability > audit verbosity
```

A class/file inventory, schema dump, or audit matrix alone is not architecture. `BASELINE_READY` requires the reverse-engineering quality validator to pass.

Material source claims require repo-relative evidence paths; add symbols/config keys where applicable.

## Output Discipline

Write detailed findings to repository artifacts.
Console output should normally contain only:

- readiness/review status
- major verified findings
- HIGH/CRITICAL blockers
- artifact paths
- exact next action


## 4.0 Detailed Design / WBS Rules

For requirement-driven implementation planning:

```text
verified TDD
→ artifact registry
→ one detailed design per artifact
→ independent DD verification
→ WBS
→ independent WBS verification
→ readiness certification
```

Never generate WBS from TDD alone when the workflow requires artifact-level detailed design.

Every WBS task must trace back to approved design.
Every verified design artifact must have WBS coverage.
Actively search for missing work; do not only review existing WBS rows.

Do not estimate effort unless the user explicitly invokes a separate estimation method.


## 4.0 Use-Case Routing

Prefer:

```text
user goal
→ `docs/USE_CASE_CATALOG.md`
→ workflow
→ stage prompt
→ skills
```

Do not ask the user to select from many skills when a documented workflow covers the task.
Use the smallest workflow sufficient for the goal.


## 4.0 Physical Layout

Use:
- `.github/` for Copilot-specific agent/skill/instruction assets
- `.ai-engineering/` for workflows/prompts/schemas/state templates
- `docs/reverse-engineering/` for generated project artifacts

All workflow/prompt references must use the 4.0 `.ai-engineering/...` paths.


## 4.0 Technical Design Architecture Gate

For requirement-driven technical design, never treat a prose-only design as reviewer-grade.

Require:
- `CURRENT Static Architecture`
- `PROPOSED Static Architecture`
- `Component Responsibilities`
- runtime sequence/flow for materially changed behavior

A static architecture section is mandatory even when the resulting structure is unchanged;
in that case explicitly state and justify the unchanged structure.

Do not advance from TDD generation to test design without independent
`technical-design-verification`.


## 4.0 Post-Readiness Audit

After `IMPLEMENTATION_READY`, follow the workflow into the independent post-readiness audit.

Do not manually ask the user for WBS IDs when workflow state can resolve the WBS and related
artifacts.

A whole-package audited PASS is the preferred implementation handoff condition.


## Package maintenance rule
Before changing/releasing the agent package, re-read `docs/PACKAGE_MAINTENANCE_RULES.md` and `docs/METHODOLOGY_BASELINE.md` from the exact predecessor package.

## Runtime methodology immutability (4.0)

During normal repository analysis/reverse-engineering execution, treat `.ai-engineering/` and `.github/` as read-only methodology infrastructure. Do not create temporary/helper prompts, workflows, skills, or agents there. Write runtime outputs only to workflow-declared artifact/state paths. If a required methodology asset is missing, stop and report it instead of synthesizing one. This restriction does not apply when the user explicitly asks to maintain or modify the methodology package itself.


### Mermaid correctness

Generated Mermaid is executable documentation, not decorative prose. Never mix Mermaid grammars:
`graph`/`flowchart` diagrams use `-->` / `-->|label|`; `sequenceDiagram` uses `->>` / `-->>` with
`: message`. A mandatory diagram that is syntactically invalid does not satisfy a quality gate.


### Preserve diagram semantics

Do not change a required diagram's semantic type to work around Mermaid syntax errors.
Component Architecture and boundary/context artifacts remain graph/flowchart representations;
Primary Runtime Sequence remains `sequenceDiagram`; lifecycle artifacts remain lifecycle/state
representations when evidence supports them. Repair grammar inside the required representation.
A syntactically valid diagram of the wrong semantic type does not satisfy the quality gate.
