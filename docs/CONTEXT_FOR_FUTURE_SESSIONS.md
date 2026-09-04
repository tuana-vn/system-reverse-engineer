# Current Session Context — System Reverse Engineer 4.0

## Purpose

This file provides only the current operating context needed to continue work in a fresh ChatGPT/Copilot session. It is not a release history or change log.

## Agent identity

System Reverse Engineer is an evidence-first backend engineering agent for understanding existing applications and producing implementation-ready engineering plans without mutating product source during analysis.

Primary backend targets:

- Java
- .NET
- C/C++
- Python

The methodology remains language-neutral unless a workflow explicitly requires toolchain-specific evidence.

## Source-of-truth hierarchy

For CURRENT behavior, prefer:

1. current repository source/configuration/build artifacts
2. runtime evidence supplied for the task
3. promoted reverse-engineering baseline artifacts
4. verified workflow artifacts
5. requirements and design documents only for intended/proposed behavior

Generated prose, hypotheses, remembered chat context, and prior verdicts are never stronger than current source.

## Core methodology

- separate discovery from certification
- isolate scope before tracing
- trace control flow and field/data provenance
- close Boundary -> Exposure paths when external reachability matters
- resolve source-resolvable HIGH/CRITICAL unknowns before downstream design
- use independent verification for requirement gaps, TDD, detailed design, WBS, and readiness
- keep CURRENT and PROPOSED facts distinct
- persist workflow state and artifacts in repository files, not conversational memory

## Workflow control plane

Declarative workflows live under `.ai-engineering/workflows/` and are executed by `run-engineering-workflow`.

Each workflow owns one authoritative YAML state path. The runner executes one substantive stage at a time, validates exactly one structured `WORKFLOW_GATE`, persists state, and follows only declared transitions.

Unknown-resolution branches bind the exact blocking artifact, blocking Q-IDs, and retry step from persisted runner state. They must not infer those values from conversation context.

Fresh child workflows re-read their workflow, prompts, skills, source artifacts, and repository from disk and do not inherit a prior verdict as proof.

## Main operating paths

Use the smallest workflow that fits the task:

- `targeted-source-analysis` for one bounded technical question
- `patch-impact-to-tests` for patch/diff impact and regression design
- `requirement-to-design` for source-backed requirement gap analysis and TDD
- `design-to-implementation` for verified TDD -> detailed design -> WBS -> readiness -> fresh post-readiness audit
- `requirement-to-implementation-plan` for the composed requirement-to-ready path
- `full-reverse-engineering` when a repository baseline is genuinely needed
- specialized workflows for claim justification, drift/rebaseline, incident RCA, and observability traceability

## State and resume

A fresh session must rehydrate from repository artifacts. Never rely on another session's memory.

Full reverse engineering uses:

`docs/reverse-engineering/workflow_state.yaml`

Run-scoped workflows normally use:

`docs/reverse-engineering/runs/<run_id>/workflow_state.yaml`

Do not create Markdown mirrors of workflow state.

## Implementation boundary

The package stops at evidence-backed planning/readiness. `IMPLEMENTATION_READY` and a passing post-readiness audit are handoff gates; they do not authorize autonomous product-source implementation, commit, merge, deployment, or production mutation.

## Package maintenance

Before changing methodology assets, read `docs/METHODOLOGY_BASELINE.md` and `docs/PACKAGE_MAINTENANCE_RULES.md`. Runtime engineering workflows treat `.ai-engineering/` and `.github/` as read-only methodology infrastructure.


## Full Reverse-Engineering Quality Contract

The canonical full-baseline consumer artifact is `docs/reverse-engineering/CURRENT_STATE_TDD.md`, not the readiness audit.

UC-01 requires five evidence-linked Mermaid diagram artifacts (system context, component architecture, primary runtime sequence, integration boundaries, state/persistence/lifecycle) plus canonical component/runtime-flow/integration/configuration/persistence-state models.

`BASELINE_READY` requires `.ai-engineering/tools/validate-reverse-engineering-quality.py` to pass.

Recommended Copilot CLI invocation:

```bash
copilot --mode autopilot --max-autopilot-continues 20
```

Select `system-reverse-engineer` with `/agent`, then:

```text
/run-engineering-workflow .ai-engineering/workflows/full-reverse-engineering.yaml run_id=YYYYMMDD
```
