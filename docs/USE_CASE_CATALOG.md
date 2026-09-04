# Use Case Catalog — System Reverse Engineer 4.0

## Why this exists

4.0 has many skills. A user should not need to memorize which skill to call.

Use this catalog to start from the engineering problem:

```text
What am I trying to achieve?
→ choose Use Case
→ run its workflow
→ workflow chooses prompts + skills + gates
```

The catalog is operational guidance, not technical evidence about the target system.

---

## Use Case Matrix

| ID | Use Case | Start When | Preferred Workflow | Primary Output | Stop / Success |
|---|---|---|---|---|---|
| UC-01 | Build/rebuild current-system baseline | Repository is unfamiliar or baseline is missing/untrusted | `full-reverse-engineering.yaml` | canonical reverse-engineering baseline | `BASELINE_READY*` |
| UC-02 | Resume previous reverse engineering | New Copilot session; repository artifacts already exist | direct `/resume-reverse-engineering` or parent workflow | rehydrated working context | resume state recovered |
| UC-03 | Answer one source-backed technical question | Need one flow/config/integration/data answer, not full baseline | `targeted-source-analysis.yaml` | targeted analysis artifact | `TARGETED_ANALYSIS_COMPLETE` |
| UC-04 | Review patch/diff impact | Patch exists; need impacted runtime/external surfaces | `patch-impact-to-tests.yaml` | patch impact + tests; compliance when requirement supplied | test design complete |
| UC-05 | Check requirement against current/proposed change | Requirement exists and current/patch behavior must be compared | `requirement-to-design.yaml` for design work, or patch workflow when patch exists | gap/compliance artifact | `DESIGN_READY*` / compliance complete |
| UC-06 | Requirement → source-backed TDD | Need technical design before implementation | `requirement-to-design.yaml` | current state + gap + TDD + contract/regression test design | workflow complete |
| UC-07 | Existing verified TDD → implementation plan | TDD already exists | `design-to-implementation.yaml` | artifact DDs + verified WBS + readiness | `IMPLEMENTATION_READY*` |
| UC-08 | Requirement → implementation-ready plan | Want end-to-end controlled planning | `requirement-to-implementation-plan.yaml` | full evidence/design/WBS/test chain | implementation readiness |
| UC-09 | Prove/narrow a high-impact claim | A semantic/architecture statement must be justified | `claim-justification.yaml` | claim verification artifact | proven/narrowed/not proven |
| UC-10 | Detect architecture drift and rebaseline | Source changed after baseline was promoted | `architecture-drift-rebaseline.yaml` | drift + verified rebaseline report | `REBASELINE_COMPLETE` |
| UC-11 | Incident root-cause investigation | Logs/runtime symptom/incidents need source-backed mechanism analysis | `incident-root-cause-analysis.yaml` | RCA artifact | complete or explicit evidence-limited result |
| UC-12 | Audit/log/metric/trace provenance analysis | Need to understand observability behavior/current gaps | `observability-traceability-analysis.yaml` | observability trace artifact | trace complete |
| UC-13 | Trace config source/precedence | Exact config value changes runtime behavior | `targeted-source-analysis.yaml` + `/configuration-source-trace` | targeted config provenance | source/default/override/consumer proven |
| UC-14 | Prove runtime implementation binding | Interface has multiple implementations or environment-dependent wiring | `targeted-source-analysis.yaml` + `/runtime-binding-verification` | binding evidence | active binding proven or unknown |
| UC-15 | Reconstruct integration selection/routing | Need exact rules selecting payment providers, inventory adapters, message transports, or native backends. | `targeted-source-analysis.yaml` + `/integration-selection-analysis` | selection matrix | rules/source anchors proven |
| UC-16 | Reverse engineer persistence/schema usage | Need source-backed DB/table/key/read/write semantics | `targeted-source-analysis.yaml` + `/persistence-schema-reverse-engineering` | persistence analysis | source-backed schema/use paths |

---

# UC-01 — Full Current-System Baseline

Use when:
- repository is unfamiliar
- existing baseline may be stale/unreliable
- later engineering work needs a trusted current-state model

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/full-reverse-engineering.yaml
```

Do not use when:
- you only need one narrow source-backed answer
- a good baseline already exists and a targeted workflow is enough

Core skills:
- `full-reverse-engineering`
- bootstrap/resume
- runtime/config/binding/integration/persistence analysis
- claim verification
- unknown closure
- coverage/adversarial audit

---

# UC-03 — Targeted Source Analysis

Use when the question is narrow, for example:

```text
Which REST endpoints can trigger the order repricing path?
Where is the final discount amount computed?
Which implementation of InventoryGateway is active?
What selects one payment provider or inventory adapter over another?
Where is the checkout timeout defaulted and overridden?
```

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/targeted-source-analysis.yaml

Inputs:
scope=<human-readable scope>
scope_slug=<safe-name>
analysis_question=<exact question>
source_anchor=<optional file/class/method>
analysis_mode=<optional runtime/config/binding/integration/persistence>
```

The workflow must not expand into a speculative redesign.

---

# UC-04 — Patch Impact Review

This is a high-value/battle-tested path.

Use when:
- a patch/diff already exists
- need runtime impact and all externally exposed surfaces
- need regression/contract test design
- optionally need requirement compliance

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/patch-impact-to-tests.yaml

Inputs:
patch_path=<diff/patch>
scope=<scope>
scope_slug=<safe-name>
requirement_path=<optional>
```

Mandatory methodology:
- patch change → runtime impact
- Boundary → Exposure Closure
- field/data provenance
- before-vs-after behavior
- scope isolation
- counterexample search
- no representative-endpoint shortcut

---

# UC-06 — Requirement to TDD

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/requirement-to-design.yaml

Inputs:
requirement_path=<path>
scope=<scope>
scope_slug=<safe-name>
```

Lifecycle:

```text
current state
→ gap analysis
→ resolve source gaps
→ TDD
→ test design
```

Do not jump directly to design.

---

# UC-07 — Existing TDD to Implementation Plan

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/design-to-implementation.yaml

Inputs:
requirement_path=<path>
current_state_artifact=<path>
gap_artifact=<path>
tdd_path=<path>
scope=<scope>
scope_slug=<safe-name>
```

Lifecycle:

```text
TDD verification
→ design artifact registry
→ DD per artifact
→ independent DD verification
→ WBS
→ WBS verification
→ implementation readiness
```

---

# UC-08 — Requirement to Implementation-Ready Plan

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/requirement-to-implementation-plan.yaml

Inputs:
requirement_path=<path>
scope=<scope>
scope_slug=<safe-name>
```

Use this only when the end-to-end lifecycle is desired.
For a quick one-question investigation, use UC-03 instead.

---

# UC-09 — Claim Justification

Examples:

```text
"All checkout requests use the same payment provider."
"The C++ pricing engine preserves rounding behavior after the library upgrade."
"No REST endpoint is affected by the Python worker change."
"The promotion field is returned only for eligible orders."
```

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/claim-justification.yaml

Inputs:
claim=<exact statement>
scope=<scope>
scope_slug=<safe-name>
requirement_path=<optional>
```

Do not broaden/narrow the claim silently.
If exact wording cannot be proven, produce the narrowest supported replacement.

---

# UC-10 — Architecture Drift / Rebaseline

Run after meaningful repository change when promoted current-state documentation may be stale.

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/architecture-drift-rebaseline.yaml

Inputs:
scope=<scope>
scope_slug=<safe-name>
change_range=<optional commit/tag/range>
```

Rebaseline only after adversarial/coverage gates pass.

---

# UC-11 — Incident Root Cause

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/incident-root-cause-analysis.yaml

Inputs:
incident_input=<log/report/evidence path>
scope=<scope>
scope_slug=<safe-name>
```

An evidence-limited result is valid.
Do not invent a definitive root cause.

---

# UC-12 — Observability / Audit / Traceability

Use for audit/log/metric/trace questions.

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/observability-traceability-analysis.yaml

Inputs:
analysis_question=<exact question>
scope=<scope>
scope_slug=<safe-name>
requirement_path=<optional>
```

Trace:
`trigger → context/provenance → decision → emission → sink → observable record`.

---

# Choosing Between Similar Use Cases

| Situation | Use |
|---|---|
| "Understand this entire legacy repo" | UC-01 |
| "Where does this field come from?" | UC-03 |
| "What does this patch affect?" | UC-04 |
| "Does this implementation satisfy this requirement?" | UC-04 with requirement if patch exists; otherwise UC-05/06 |
| "Design this requirement" | UC-06 |
| "I already have TDD; make DD/WBS" | UC-07 |
| "Take requirement all the way to implementation-ready" | UC-08 |
| "Prove this architecture statement" | UC-09 |
| "Repo changed; is baseline stale?" | UC-10 |
| "Why did production fail?" | UC-11 |
| "Where/how is this audit log emitted?" | UC-12 |

---

# General Rule

Start with the smallest use case that can answer the question safely.

Do not run a full workflow merely because more skills exist.
Do not call individual skills manually when a suitable controlled workflow already exists.


---

# UC-17 — Post-Readiness Adversarial Audit

Use when:

- `design-to-implementation` already reached `IMPLEMENTATION_READY`, or
- a completed planning package must be independently challenged before handoff to a developer agent.

Run:

```text
Use /run-engineering-workflow.

Run:
.ai-engineering/workflows/post-readiness-audit.yaml

Inputs:
source_run_id=<completed design-to-implementation run id>
source_workflow_state=docs/reverse-engineering/workflows/<run-id>.yaml
requirement_path=<authoritative requirement path>
scope=<human-readable scope>
scope_slug=<safe-name>
```

For `design-to-implementation` runs, this audit is invoked automatically after
implementation readiness.

The audit independently checks:

```text
workflow/gate integrity
→ deterministic WBS backward traces
→ proposed architecture consistency
→ negative/MUST-NOT rules
→ boundary exposure closure
→ WBS missing work
→ source-anchor health
→ quantitative scorecard
```

The user should not manually select WBS IDs.

Success:

```text
POST_READINESS_AUDIT_PASS
POST_READINESS_AUDIT_PASS_WITH_WARNINGS
```

A failed post-readiness audit blocks downstream implementation handoff until the owning
upstream artifact/workflow is corrected and the audit reruns.
