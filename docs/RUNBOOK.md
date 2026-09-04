# System Reverse Engineer 4.0 — Operational Runbook

## 0. Purpose

This runbook answers one practical question:

> "I have engineering problem X. What exactly do I run?"

Do not start by browsing 29 skills.

Use:

```text
problem
→ use case
→ workflow
→ prompts + skills selected by workflow
→ artifacts + gates
```

Reference:
- `docs/USE_CASE_CATALOG.md`
- `docs/WORKFLOW_MATRIX.md`
- `docs/SKILL_MATRIX.md`
- `docs/USE_CASE_SKILL_WORKFLOW_MATRIX.md`

---

## 1. First-Time Installation

Install the agent/.github/skills/instructions into the target repository according to `README.md`.

Keep these package directories accessible in the target repository:

```text
.ai-engineering/workflows/
.ai-engineering/prompts/
.ai-engineering/schemas/
```

The workflows reference prompt files by repository-relative path.

---

## 2. Before Every Run

Check:

```text
[ ] exact target repository/source is open
[ ] requirement/patch/log path is known when required
[ ] scope is explicit
[ ] scope_slug is filesystem-safe
[ ] generated reverse-engineering artifacts from previous runs are available if this is a continuation
```

If the current-system baseline already exists:

```text
Use /resume-reverse-engineering.
```

Do not rebuild the whole baseline automatically unless UC-01 is actually needed.

---

## 3. Workflow Invocation Pattern

Use this shape:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/<workflow>.yaml

Inputs:
key=value
key=value
```

Do not copy/paste the full prompt file when the prompt already exists in the repository.

The runner must:
1. load workflow
2. execute one substantive stage
3. write artifact
4. read structured `WORKFLOW_GATE`
5. persist state
6. transition/retry/stop

A missing gate is not success.

---

## 4. Fast Use-Case Selector

| What you need | Run |
|---|---|
| Understand whole repository / build trusted baseline | `.ai-engineering/workflows/full-reverse-engineering.yaml` |
| Answer one exact source question | `.ai-engineering/workflows/targeted-source-analysis.yaml` |
| Review a patch and create tests | `.ai-engineering/workflows/patch-impact-to-tests.yaml` |
| Requirement → TDD + tests | `.ai-engineering/workflows/requirement-to-design.yaml` |
| Existing TDD → detailed design + WBS | `.ai-engineering/workflows/design-to-implementation.yaml` |
| Requirement → implementation-ready plan | `.ai-engineering/workflows/requirement-to-implementation-plan.yaml` |
| Prove one important claim | `.ai-engineering/workflows/claim-justification.yaml` |
| Source changed; detect drift/rebaseline | `.ai-engineering/workflows/architecture-drift-rebaseline.yaml` |
| Investigate incident/root cause | `.ai-engineering/workflows/incident-root-cause-analysis.yaml` |
| Trace logging/audit/metric behavior | `.ai-engineering/workflows/observability-traceability-analysis.yaml` |

---

## 5. UC-01 — Full Reverse Engineering Baseline

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/full-reverse-engineering.yaml
```

Use when:
- repository is unfamiliar
- baseline is absent/untrusted
- broad architecture understanding is required

Expected canonical workspace:

```text
docs/reverse-engineering/
  00_current_understanding.md
  00_evidence_ledger.md
  00_master_decision_matrix.md
  00_hypotheses.md
  00_open_questions.md
  workflow_state.yaml
  00_investigation_coverage.md
```

Do not call `BASELINE_READY` with unresolved source-resolvable HIGH/CRITICAL gaps.

---

## 6. UC-03 — Targeted Source Analysis

Example:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/targeted-source-analysis.yaml

Inputs:
scope=Order discount response behavior
scope_slug=order_discount_response
analysis_question=Trace exactly where the discount amount is calculated and under what endpoint/request conditions it appears.
analysis_mode=runtime
```

For specialized questions, the prompt may invoke:
- config source trace
- runtime binding
- integration selection
- persistence schema

Use this instead of full RE for one narrow question.

---

## 7. UC-04 — Patch Impact Review

Without requirement:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/patch-impact-to-tests.yaml

Inputs:
patch_path=patches/change.patch
scope=Promotion-code normalization change
scope_slug=promotion_code_normalization
```

With requirement:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/patch-impact-to-tests.yaml

Inputs:
patch_path=patches/change.patch
requirement_path=requirements/promotion_code_requirement.md
scope=Promotion-code normalization change
scope_slug=promotion_code_normalization
```

Key gates:
- all changed runtime behavior traced
- Boundary → Exposure Closure
- field/data provenance where applicable
- no representative-endpoint shortcut
- requirement scope isolation
- regression/contract test coverage

---

## 8. UC-06 — Requirement → TDD

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/requirement-to-design.yaml

Inputs:
requirement_path=requirements/cart_validation.md
scope=Cart validation rule
scope_slug=feature_x
```

Lifecycle:

```text
current-state analysis
→ requirement gap analysis
→ resolve high-impact source gaps
→ technical design
→ independent TDD verification
→ contract/regression test design
```

The TDD must contain `PROPOSED Static Architecture` and pass architecture consistency verification before test design.

Do not jump directly to TDD.

---

## 9. UC-07 — Existing TDD → Detailed Design / WBS

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/design-to-implementation.yaml

Inputs:
requirement_path=requirements/feature.md
current_state_artifact=docs/reverse-engineering/analysis/feature_x_current_state.md
gap_artifact=docs/reverse-engineering/analysis/feature_x_requirement_gap.md
tdd_path=docs/reverse-engineering/proposals/feature_x_tdd.md
scope=Feature X
scope_slug=feature_x
```

Lifecycle:

```text
TDD verification
→ design artifact registry
→ one DD per artifact
→ independent DD verification
→ WBS
→ independent WBS verification
→ implementation readiness
```

WBS is not effort estimation.

---

## 10. UC-08 — Requirement → Implementation-Ready Plan

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/requirement-to-implementation-plan.yaml

Inputs:
requirement_path=requirements/cart_validation.md
scope=Cart validation rule
scope_slug=feature_x
```

Use only when you want the entire planning chain.
For a narrow task, choose a smaller workflow.

---

## 11. UC-09 — Claim Justification

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/claim-justification.yaml

Inputs:
claim=All write APIs can reach the CLI integration path.
scope=Checkout API integration exposure
scope_slug=write_api_cli_exposure
```

The exact claim may be:
- proven
- partially proven
- contradicted
- not proven
- source not resolved

Do not convert a narrower proven statement into the original broader claim.

---

## 12. UC-10 — Architecture Drift / Rebaseline

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/architecture-drift-rebaseline.yaml

Inputs:
scope=Current system baseline
scope_slug=current_system
change_range=<optional>
```

Stages:
```text
detect drift
→ adversarial/coverage verification
→ rebaseline only if ready
```

---

## 13. UC-11 — Incident RCA

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/incident-root-cause-analysis.yaml

Inputs:
incident_input=evidence/python_worker_memory_incident.md
scope=Python worker memory growth
scope_slug=production_oom
```

A partial/evidence-limited conclusion is acceptable.

Never force a root cause when evidence only supports candidate causes.

---

## 14. UC-12 — Observability / Audit Trace

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/observability-traceability-analysis.yaml

Inputs:
analysis_question=Where is the authenticated user identity available and where is order-change audit logging emitted?
scope=Order-change audit logging
scope_slug=order_change_audit_logging
requirement_path=requirements/order_audit.md
```

Trace:
```text
trigger
→ context/data provenance
→ decision
→ emission
→ sink
→ observable record
```

---

## 15. Resume a Blocked/Interrupted Workflow

Use the persisted workflow state under:

```text
docs/reverse-engineering/.ai-engineering/workflows/<run-id>.yaml
```

Then:

```text
Use /run-engineering-workflow.

Resume workflow run:
<run-id>
```

The agent must use persisted state and artifacts.
It must not reconstruct completion from chat memory.

---

## 16. When a Workflow Blocks

### Source-resolvable HIGH/CRITICAL unknown

Run the workflow-defined resolver loop.

Do not bypass it.

### External blocker

Record:
- exact missing evidence
- why repository source cannot resolve it
- which claim/decision is blocked

### Design contradiction

Return to the design stage.
Do not let implementation planning silently redesign it.

### Verification failure

Use:
```text
generate
→ verify independently
→ findings
→ revise
→ reverify
```

Do not let verifier silently edit its own target.

---

## 17. Artifact Trust Rule

Generated artifact ≠ current-system truth by itself.

For high-impact downstream decisions:
- keep evidence refs
- reverify current source where necessary
- never trust "previous agent said so"

---

## 18. Minimal Command Cheat Sheet

```text
# full baseline
Run .ai-engineering/workflows/full-reverse-engineering.yaml

# one technical question
Run .ai-engineering/workflows/targeted-source-analysis.yaml

# patch
Run .ai-engineering/workflows/patch-impact-to-tests.yaml

# requirement → TDD
Run .ai-engineering/workflows/requirement-to-design.yaml

# TDD → DD/WBS
Run .ai-engineering/workflows/design-to-implementation.yaml

# end-to-end planning
Run .ai-engineering/workflows/requirement-to-implementation-plan.yaml

# claim
Run .ai-engineering/workflows/claim-justification.yaml

# drift
Run .ai-engineering/workflows/architecture-drift-rebaseline.yaml

# incident
Run .ai-engineering/workflows/incident-root-cause-analysis.yaml

# audit/log/trace
Run .ai-engineering/workflows/observability-traceability-analysis.yaml
```

See `docs/USE_CASE_CATALOG.md` for decision guidance and `docs/SKILL_MATRIX.md` when you need to understand the skills behind a workflow.


---

## 19. UC-17 — Post-Readiness Adversarial Audit

### Behavior

`design-to-implementation.yaml` now continues automatically:

```text
implementation readiness
→ post-readiness adversarial audit
→ DONE only when post-audit passes
```

No manual WBS-ID prompt is required.

For an existing completed run that must be independently audited:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/post-readiness-audit.yaml

Inputs:
source_run_id=<completed run id>
source_workflow_state=docs/reverse-engineering/workflows/<run-id>.yaml
requirement_path=<path>
scope=<scope>
scope_slug=<safe-name>
```

Expected output:

```text
docs/reverse-engineering/audits/<scope_slug>_post_readiness_audit.md
```

Required audit thresholds include:

```text
valid required stages/gates                 = 100%
implementation-required DD verified         = 100%
sampled WBS backward traces complete        = 100%
major architecture components covered       = 100%
explicit negative rules covered             = 100%
affected boundary exposure closure           = 100%
critical/source anchors sampled verified     = 100%
source-resolvable CRITICAL unknowns          = 0
source-resolvable HIGH unknowns              = 0
HIGH/CRITICAL missing-work findings          = 0
```

Downstream implementation handoff should use an audited PASS, not readiness prose alone.

## Package validation

Run:

```bash
python .ai-engineering/tools/validate-package-layout.py
python .ai-engineering/tools/validate-methodology-baseline.py
python .ai-engineering/tools/validate-workflow-contracts.py
```

Use `--strict-package-root` on the extracted delivery package.
