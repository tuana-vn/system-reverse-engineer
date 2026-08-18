---
name: resume-reverse-engineering
description: Rehydrate a fresh Copilot session from the existing V3.0 repository-backed reverse-engineering baseline and workflow state without restarting reverse engineering from scratch.
license: MIT
---

# Resume Reverse Engineering — V3.0

## Purpose

Use this skill at the beginning of a NEW Copilot session when reverse-engineering work already exists in the repository.

The previous Copilot session is NOT a source of truth.

The repository is the persistent memory.

This skill restores working context from the existing V3.0 artifacts so that subsequent skills can continue from the current verified baseline.

## Core Rule

```text
FRESH SESSION
    ↓
REHYDRATE FROM REPOSITORY
    ↓
LOAD PROMOTED BASELINE
    ↓
LOAD WORKFLOW STATE
    ↓
LOAD ONLY RELEVANT SUPPORTING ARTIFACTS
    ↓
CONTINUE WITH NEXT V3.0 SKILL
```

Do NOT restart `/full-reverse-engineering` merely because the session is new.

Do NOT rely on conversational memory from another Copilot session.

Do NOT treat hypotheses, proposals, drafts, or rejected findings as promoted architecture facts.

## Step 1 — Load V3.0 Operating Instructions

Read, when present:

```text
.github/copilot-instructions.md
```

Read the active `system-reverse-engineer` agent instructions.

Read this skill and any V3.0 skill explicitly referenced by the current workflow state.

Do not load every skill into working context unless necessary.

## Step 2 — Locate the Canonical Reverse-Engineering Workspace

Locate:

```text
docs/reverse-engineering/
```

Prefer the repository's existing paths and filenames.

Do not invent replacement files if equivalent V3.0 files already exist.

Identify the current canonical artifacts, especially:

```text
00_current_understanding.md
00_master_decision_matrix.md
00_evidence_ledger.md
00_hypotheses.md
00_open_questions.md
00_workflow_state.md
00_investigation_coverage.md
```

Also locate, when present:

```text
02_representative_runtime_flows.md
03_integration_selection.md
04_boundaries.md
05_error_retry_fallback.md
07_adversarial_baseline_audit.md
08_final_reverse_engineered_baseline.md
```

If filenames differ slightly in the repository, use the actual V3.0 files rather than creating duplicates.

## Step 3 — Establish Baseline Identity

Determine the source identity associated with the existing baseline.

Prefer, in order:

1. baseline commit recorded in V3.0 artifacts
2. repository commit recorded in workflow state
3. current Git HEAD if no baseline identity is recorded

Report:

```text
repository
branch
current HEAD
baseline commit/version
```

If current HEAD differs from the recorded baseline, DO NOT silently assume the baseline is current.

Record the difference in the resume summary.

Do not automatically run baseline maintenance.

## Step 4 — Rehydrate Canonical Knowledge

Load and summarize internally:

### Promoted architecture facts

From:

```text
00_current_understanding.md
```

Only promoted/verified knowledge is treated as established architecture.

### Routing / selection facts

From:

```text
00_master_decision_matrix.md
```

Use only promoted routing decisions.

### Evidence history

From:

```text
00_evidence_ledger.md
```

Use this to understand:
- claim IDs
- verification status
- superseded/rejected claims
- baseline version
- promotion state

Do not promote a claim during resume.

### Hypotheses

From:

```text
00_hypotheses.md
```

Treat these as NON-CANONICAL.

### Open questions

From:

```text
00_open_questions.md
```

Use these only to understand unresolved work.

Do not assume an old open question is still unresolved if current source or later artifacts already resolved it.

### Workflow state

From:

```text
00_workflow_state.md
00_investigation_coverage.md
```

Determine:
- completed phases
- current phase
- pending phase
- last successful skill/workflow
- known blockers
- expected next action
- baseline readiness status
- HIGH/CRITICAL unknowns and closure states
- coverage gaps from `00_investigation_coverage.md`

If any HIGH/CRITICAL item is `SOURCE_SEARCH_PENDING` or `SOURCE_SEARCH_IN_PROGRESS`, do not report the baseline as ready. Recommend `/resolve-high-impact-unknowns`.

## Step 5 — Load Only Relevant Supporting Evidence

Do NOT flood the context with the entire reverse-engineering repository.

Based on the current workflow state and the user's next task, selectively read supporting artifacts.

Examples:

### Runtime-flow task
Read:
```text
02_representative_runtime_flows.md
```

### Integration/boundary task
Read:
```text
03_integration_selection.md
04_boundaries.md
```

### Failure/retry task
Read:
```text
05_error_retry_fallback.md
```

### Baseline trust/review task
Read:
```text
07_adversarial_baseline_audit.md
08_final_reverse_engineered_baseline.md
```

### Patch/design/review task
Load only the baseline sections and evidence relevant to the changed feature or subsystem.

Current source remains authoritative whenever re-verification is required.

## Step 6 — Detect Staleness Without Rebuilding the Baseline

Check whether the repository has materially changed since the recorded baseline.

Use lightweight Git/source inspection.

Examples:
- current HEAD differs from baseline commit
- files referenced by promoted claims changed
- relevant integration classes changed
- branch changed

Classify:

```text
BASELINE_CURRENT
BASELINE_POTENTIALLY_STALE
BASELINE_STALE_FOR_CURRENT_TASK
```

Do NOT automatically run `/baseline-source-of-truth-maintenance`.

If maintenance is needed, recommend it as the next V3.0 action.

For a patch or unmerged diff, do NOT treat patch behavior as current canonical truth.

## Step 7 — Resume State

Produce an internal working state containing:

```text
Baseline identity
Promoted architecture summary
Relevant decision-matrix entries
Relevant evidence IDs
Relevant unresolved questions
Workflow phase/status
Baseline freshness
Baseline readiness
High-impact unknown closure state
Likely next V3.0 skill
```

Do not create a new reverse-engineering baseline during resume.

Do not update canonical files.

## Search Discipline

If a referenced artifact says something is UNKNOWN but the user's next task requires that fact:

```text
baseline UNKNOWN
    ↓
inspect CURRENT SOURCE
    ↓
resolve if source contains the answer
```

Do not preserve an UNKNOWN merely because an old document contained it.

However, this resume skill itself should remain lightweight.

Deep source tracing belongs to the subsequent task skill unless the fact is necessary to determine the correct resume state.

## Canonical vs Non-Canonical Inputs

### Canonical

Prefer:

```text
promoted current understanding
promoted decision matrix
evidence ledger promoted claims
verified final baseline
current source
```

### Non-canonical unless explicitly verified

Do NOT use as architecture truth merely because they exist:

```text
proposals/
draft TDDs
patch review outputs
requirement review outputs
hypotheses
rejected designs
temporary notes
AI-generated reports
unmerged patches
```

These may be task inputs, but they do not replace the promoted baseline.

## Completion Output

Do NOT print a large baseline dump to console.

Return only a concise resume summary:

```text
Reverse-engineering context resumed.

Baseline:
- Commit/version: ...
- Current HEAD: ...
- Freshness: BASELINE_CURRENT | BASELINE_POTENTIALLY_STALE | BASELINE_STALE_FOR_CURRENT_TASK

Workflow:
- Last completed phase: ...
- Current/pending phase: ...

Relevant architecture:
- <3-8 concise points relevant to the likely/current task>

Open items relevant to continuation:
- <only relevant unresolved items>

Ready for:
- /<recommended-next-skill>
```

If the user has already supplied a task in the same prompt, do NOT wait.

After rehydrating context, immediately execute the requested V3.0 skill.

Example:

```text
Use /resume-reverse-engineering, then use /patch-impact-review for patch/abc.diff.
```

In that case:
1. resume context
2. do not print a separate long resume report
3. execute `/patch-impact-review`
4. return the normal output of that skill

## Safety / Integrity Rules

Never:
- restart full reverse engineering solely because this is a fresh session
- promote hypotheses during resume
- overwrite canonical baseline
- infer old chat context that is absent from repository
- treat proposal documents as promoted evidence
- treat unmerged patch code as current baseline
- silently ignore baseline/current-HEAD mismatch

The repository-backed V3.0 baseline is the persistent memory.
The Copilot conversation is disposable working context.
