---
name: full-reverse-engineering
description: Methodology reference for the repository-wide source-first reverse-engineering baseline. Full execution is controlled by .ai-engineering/workflows/full-reverse-engineering.yaml through /run-engineering-workflow.
---

# Full Reverse Engineering — Methodology Reference

## Purpose

Build a deep, source-backed CURRENT-system baseline from repository source plus runtime/config/test evidence when available.

The execution entry point is the existing declarative workflow:

```text
.ai-engineering/workflows/full-reverse-engineering.yaml
```

Run it through `/run-engineering-workflow`.

## Critical Execution Boundary

This skill is **not** a nested-skill orchestrator.

During a reverse-engineering run:

- do NOT generate helper prompts under `.ai-engineering/prompts/`;
- do NOT generate helper workflows under `.ai-engineering/workflows/`;
- do NOT generate or modify skills under `.github/skills/`;
- do NOT modify `.github/agents/` or `.github/copilot-instructions.md`;
- do NOT translate this skill into temporary workflow/prompt files;
- do NOT invoke slash sub-skills from this document.

The workflow already names the existing skills to apply at each stage. Apply those skills directly to the repository evidence and write only the workflow-declared reverse-engineering artifacts/state.

If a required methodology asset is missing, stop and report the missing asset. Never synthesize a replacement during a repository analysis run.

## Reasoning Model

```text
DISCOVERY
→ candidate claims
→ source verification
→ counterexample search
→ scope isolation
→ data/config/binding/boundary closure
→ evidence promotion
→ adversarial coverage/readiness audit
→ canonical CURRENT baseline
```

Current source and runtime/config evidence outrank generated Markdown.

## Deliverable Quality Principle

A reverse-engineered baseline is not complete merely because claims are verified. It must reconstruct the system into an understandable model of responsibilities, dependencies, runtime flows, state, boundaries, variants, and failure behavior.

For a full backend baseline:

```text
model > inventory
relationships > file counts
behavior > component names
diagrams > repeated prose
consumer usability > audit verbosity
```

The canonical consumer artifact is `docs/reverse-engineering/CURRENT_STATE_TDD.md`. The readiness audit is separate.

## Core Analysis Obligations

The full workflow must cover, where applicable:

- repository/startup topology and inbound surfaces;
- representative runtime control flows;
- field/data provenance for externally meaningful values;
- integration selection and concrete runtime binding;
- configuration source, defaults, override precedence, and consumers;
- real external boundaries and boundary → exposure closure;
- persistence/schema/data lifecycle;
- validation/error/retry/fallback behavior;
- resource/session/cache/thread/async lifecycle when material;
- alternate implementations, modes, branches, legacy/fallback paths, and counterexamples;
- HIGH/CRITICAL unknown closure;
- adversarial verification and coverage audit;
- consumer-facing architecture synthesis;
- mandatory Mermaid system-context, component, runtime-sequence, integration-boundary, and state/persistence/lifecycle diagrams;
- a canonical Current-State TDD suitable as source-of-truth input to a later Design Agent.

## Evidence Discipline

Every material finding is one of:

```text
CANDIDATE
VERIFIED / PROMOTED
HYPOTHESIS
REJECTED / SUPERSEDED
UNKNOWN with explicit closure state
```

Do not promote from filenames, class names, comments, or one representative path alone.

For observable data claims, trace:

```text
trigger
→ source/retrieval
→ parse/transform
→ mapping/state
→ serialization/output
→ observable effect
```

For integration exposure claims, trace:

```text
boundary
← invocation sites
← caller chains
← external entry points or proven internal roots
```

## Readiness

`BASELINE_READY` is allowed only when source-resolvable HIGH/CRITICAL gaps and material adversarial contradictions are zero **and** the consumer-quality contract passes.

Consumer-quality minimum for full baseline:

```text
mandatory diagram artifacts = 5/5
material subsystem modeling = 100%
known integration boundary modeling = 100%
behavior-changing configuration classification = 100%
material evidence paths present = 100%
blocking unknowns = 0
```

Run `.ai-engineering/tools/validate-reverse-engineering-quality.py --artifact-root docs/reverse-engineering` before final readiness.

`BASELINE_READY` is allowed only when source-resolvable HIGH/CRITICAL gaps and material adversarial contradictions are zero.

`BASELINE_READY_WITH_EXTERNAL_BLOCKERS` is allowed only when every remaining HIGH/CRITICAL item is evidence-backed as externally blocked.

Otherwise use `NOT_READY_HIGH_IMPACT_GAPS` or `PARTIAL_RESUMABLE`.

## Runtime Output Boundary

Repository analysis writes reverse-engineering results under the workflow-declared `docs/reverse-engineering/...` paths only.

`.ai-engineering/` and `.github/` are methodology infrastructure and are read-only during normal reverse-engineering execution.
