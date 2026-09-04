# METHODOLOGY_BASELINE

**Status:** NORMATIVE  
**Applies to:** System Reverse Engineer 4.0.

This document defines what the agent is for, where it stops, and the quality properties that future
versions must preserve. Historical changelogs, prompts, skills, workflow mechanics, and package
versions are subordinate to this baseline.

## 1. Agent Purpose

The System Reverse Engineer exists to turn an unfamiliar or legacy system plus an engineering
requirement/problem into an evidence-backed, implementation-ready design package.

Core target:

```text
requirement / change / incident
+ current repository
+ runtime/config/test evidence when available
→ understand CURRENT truth
→ identify verified GAP / IMPACT
→ design PROPOSED solution
→ independently verify the design
→ decompose and verify implementation work
→ IMPLEMENTATION_READY
```

The target is not "complete the workflow". The target is a package that a downstream implementer can
use without inventing material design decisions.

## 1.1 Runtime Methodology Immutability

During normal reverse-engineering execution, `.ai-engineering/` and `.github/` are read-only methodology infrastructure. A runtime analysis may produce only workflow-declared analysis/state artifacts; it must not materialize skills into new prompts/workflows or otherwise mutate the methodology that governs the run. Missing methodology assets are execution errors, not invitations to synthesize replacements.

## 2. Agent Boundary

The System Reverse Engineer:

- MAY discover, analyze, verify, design, decompose, produce DD/WBS/test viewpoints, and certify readiness.
- MUST NOT silently implement production code as part of the architecture workflow.
- MUST NOT invent unresolved behavior, source facts, scope, risk, or estimates.
- MUST stop or remain explicit when evidence is insufficient.
- MUST separate WBS from effort estimation unless a separately approved estimation capability is invoked.

Canonical stop condition:

```text
IMPLEMENTATION_READY
```

Implementation is a downstream concern.

## 3. Core Methodology

The reasoning spine is:

```text
DISCOVER
→ CANDIDATE CLAIM
→ SOURCE VERIFICATION
→ COUNTEREXAMPLE SEARCH
→ SCOPE CHECK
→ EVIDENCE RECORD
→ PROMOTION GATE
→ CANONICAL BASELINE
```

Applied to engineering design:

```text
CURRENT STATE
→ GAP / IMPACT
→ PROPOSED DESIGN
→ INDEPENDENT DESIGN VERIFICATION
→ IMPLEMENTATION ARTIFACT DECOMPOSITION
→ DETAILED DESIGN + INDEPENDENT VERIFICATION
→ WBS + INDEPENDENT VERIFICATION
→ READINESS CERTIFICATION
```

Generator and verifier are separate responsibilities:

```text
generate
→ independently verify
→ correct
→ reverify
```

A generator's PASS claim is never evidence by itself.

## 4. Evidence Rules

For CURRENT behavior:

```text
current source / runtime evidence
> tests supporting the same path
> verified reverse-engineering artifacts
> documentation/comments
> hypotheses
```

For intended behavior:

```text
authoritative requirement
> approved design decision
```

Mandatory rules:

- UNKNOWN remains UNKNOWN until evidence resolves it.
- User correction is a reason to re-open the evidence trace, not evidence by itself.
- Observable behavior is more important than implementation shape.
- Field/data behavior should be traced end-to-end where material.
- Boundary impact requires exposure closure across material invocation/caller/entry paths.
- Requirement/scope conditions must not leak across endpoints/operations.
- A VERIFIED upstream artifact is a trusted input for efficiency, not immutable truth.
- Downstream stages must re-ground material upstream claims when contradiction, ambiguity, new scope,
  high impact, stale provenance, or source-commit change appears.
- A contradiction against primary evidence re-opens the upstream claim and invalidates dependent
  downstream conclusions until resolved.
- A resolved CURRENT/SOURCE fact does not automatically authorize a PROPOSED design decision.
  Any design choice derived from a source fact must be labeled PROPOSED and traced to an authoritative
  requirement/gap; absence of a current mechanism is not evidence for a specific future mechanism.

## 5. Mandatory Quality Targets

`IMPLEMENTATION_READY` is permitted only when all applicable targets are met.

| ID | Quality Target | Required Threshold |
|---|---|---|
| Q1 | Material CURRENT claims have evidence | 100% |
| Q2 | Material requirement conditions are scoped to the correct operation/row | 100% |
| Q3 | HIGH/CRITICAL claims have counterexample search where source-resolvable | 100% |
| Q4 | Material design decisions trace to verified requirement/gap | 100% |
| Q5 | Implementation-significant proposed units have explicit design ownership | 100% |
| Q6 | Implementation-required artifacts have independently VERIFIED DD | 100% |
| Q7 | WBS implementation tasks map semantically to verified design | 100% |
| Q8 | Unresolved source-resolvable HIGH/CRITICAL gaps at readiness | 0 |
| Q9 | Current/proposed architectural state contamination in verified design | 0 |
| Q10 | Downstream implementer must invent material design decisions | 0 |
| Q11 | Unauthorized effort/duration estimates in WBS | 0 |
| Q12 | Current-run gates satisfied by stale/prior-run artifacts | 0 |
| Q13 | Downstream failure attributed to a stage before its material inputs are verified | 0 |
| Q14 | Dependent downstream artifacts retained after an upstream claim is corrected | 0 |
| Q15 | Requirement-derived obligations/fields added without explicit authoritative support or PROPOSED classification | 0 |
| Q16 | TDD decision logic that fails any authoritative MUST LOG / MUST NOT LOG matrix row | 0 |
| Q17 | Workflow starts with a missing or provenance-mismatched required upstream artifact | 0 |
| Q18 | Run-scoped workflow has more than one authoritative workflow-state file | 0 |
| Q19 | Canonical requirement IDs map to more than one semantic rule within a run | 0 |
| Q20 | Executive/summary requirement-gap metrics disagree with the canonical compliance matrix | 0 |
| Q21 | Stage narrative, workflow gate, and next-step semantics contradict each other | 0 |

Qualitative labels such as LOW/HIGH/NONE risk or HIGH confidence are not sufficient evidence unless
the artifact defines measurable criteria for that label and shows the supporting evidence.

## 6. CURRENT vs PROPOSED Separation

The following are different truth domains and must remain visibly distinct:

```text
CURRENT = proven existing behavior/structure
PROPOSED = intended future behavior/structure
UNKNOWN = unresolved
```

A section or diagram labeled CURRENT must not contain a PROPOSED component/relationship as though it
already exists.

A proposed element may be shown alongside CURRENT only when the diagram is explicitly a transition or
PROPOSED view and the states are unambiguous.

## 7. Failure Investigation and Earliest-Divergence Rule

A failure observed at stage A MUST NOT be attributed to stage A until the material inputs consumed by
stage A have been verified.

Required investigation flow:

```text
OBSERVED FAILURE AT STAGE A
→ COLLECT A INPUTS + A OUTPUT
→ VERIFY A INPUTS AGAINST PRIMARY EVIDENCE / AUTHORITATIVE REQUIREMENT
→ IF AN INPUT IS ALREADY WRONG: WALK ONE STAGE UPSTREAM AND REPEAT
→ IF INPUTS ARE SOUND: A BECOMES THE CANDIDATE RESPONSIBLE LAYER
→ IDENTIFY THE EARLIEST DIVERGENCE
→ FIX ONLY THE EARLIEST RESPONSIBLE LAYER
→ INVALIDATE DEPENDENT DOWNSTREAM ARTIFACTS
→ RERUN FROM THE EARLIEST INVALIDATED STAGE
```

Normative rules:

- `EARLIEST_DIVERGENCE_WINS`.
- `NO_LOCAL_PATCH_WITHOUT_UPSTREAM_CHECK`.
- The nearest failing verifier/gate is not automatically the root cause.
- Before changing a skill, prompt, verifier, or workflow because of a downstream failure, inspect the
  failing stage's material input artifacts.
- If the defect already exists in an input artifact, do not tune the downstream stage to compensate.
  Continue tracing upstream until the first claim that diverges from primary source evidence for
  CURRENT truth or authoritative requirement for intended truth.
- If an upstream claim is corrected, every dependent downstream artifact and verdict is invalid until
  regenerated/reverified.
- When evidence needed for root-cause attribution is missing, the correct decision is
  `NOT_ENOUGH_EVIDENCE`, not a speculative methodology fix.

This rule exists specifically to prevent repeated nearest-gate tuning on top of incorrect data.

## 8. Requirement Fidelity and Source-Fact Promotion

Requirement analysis and design must preserve the boundary between obligation and proposal.

```text
AUTHORITATIVE REQUIREMENT
→ normalized requirement rule
→ verified gap/non-gap
→ PROPOSED design decision
```

Mandatory rules:

- A requirement/gap artifact MUST NOT add a mandatory field, scenario, acceptance criterion, or behavior
  unless it is explicit in the authoritative requirement.
- Source-discovered data or mechanisms may be recorded as CURRENT availability; using them in the future
  solution is a PROPOSED design choice unless the requirement explicitly mandates them.
- A PROPOSED choice must not be relabeled as SOURCE-VERIFIED merely because its inputs are source-verified.
- If the authoritative requirement is silent, preserve that silence or label the addition as PROPOSED.
- A design verifier must evaluate executable decision logic against every row in the authoritative
  MUST LOG / MUST NOT LOG matrix. Textual similarity is insufficient. Required threshold: 100% rows pass.
- Requirement identity is run-canonical. The first normalized scenario/constraint ledger assigns stable IDs;
  downstream artifacts MUST copy those IDs and semantics, not renumber or reuse them for another rule.
- Executive summaries and aggregate counts MUST be derived from the canonical compliance matrix. A generated
  summary is not an independent source of truth.
- If one requirement can carry multiple gap types, distinguish `unique_requirement_count` from
  `gap_type_occurrence_count`; do not present overlapping counts as mutually exclusive requirement totals.
- A stage gate and its narrative MUST agree. If a stage is allowed to proceed with non-blocking unknowns, the
  narrative must explicitly call them non-blocking/deferred and MUST NOT say they must be resolved before proceeding.

## 9. Workflow Input and State Preconditions

Before a downstream workflow starts, every required upstream artifact must exist and match the declared
provenance. A path string or reference in another generated document is not proof that the artifact exists.

For run-scoped workflows:

- the single authoritative state file is the workflow-declared `workflow_state.yaml`;
- no Markdown workflow-state mirror may be created inside the run directory;
- missing required inputs => `REQUIRED_INPUT_ARTIFACT_MISSING`;
- provenance/path mismatch => `UPSTREAM_PROVENANCE_MISMATCH`;
- duplicate run-state artifacts => `WORKFLOW_STATE_INTEGRITY_VIOLATION`.

## 10. Methodology vs Execution Plumbing

Methodology:

- evidence hierarchy
- source verification
- counterexample search
- scope isolation
- provenance/exposure closure
- CURRENT → GAP → DESIGN
- independent verification
- design/DD/WBS/readiness quality gates

Execution plumbing:

- workflow YAML
- status routing
- run IDs
- state files
- manifests
- stable filenames
- fresh/resume semantics
- validators

Execution plumbing exists only to execute the methodology reliably. It must not redefine the agent's
purpose or grow into a separate SDLC platform.

## 11. Change-Control Rule

Methodology changes require explicit package-maintenance intent and must preserve the agent purpose, evidence hierarchy, CURRENT/PROPOSED separation, independent verification model, and `IMPLEMENTATION_READY` stop boundary unless the user explicitly requests a boundary change.

A verified defect should be fixed at the earliest responsible layer and downstream dependent artifacts must be invalidated when necessary.

Any purpose or boundary change must be stated explicitly as:

`purpose_or_boundary_change = YES | NO`

Normal maintenance uses:

`purpose_or_boundary_change = NO`

## 12. Package Maintenance and Tooling Discipline

Package maintenance follows `docs/PACKAGE_MAINTENANCE_RULES.md`. Deterministic validators enforce generic mechanical contracts; semantic correctness remains the responsibility of independent workflow verification stages. Runtime engineering runs must not mutate methodology infrastructure.

## 13. Stage Ownership and Design-Prerequisite Source Closure

For staged requirement-to-design execution:

```text
Stage 01 CURRENT
  owns current truth + unknowns
  does NOT own gap/no-gap classification

Stage 02 GAP
  owns compliance/gap classification
  does NOT authorize technical design directly when an independent gap verifier exists

Stage 02B GAP VERIFICATION
  independently re-derives requirement identity, fidelity, aggregates, and design-prerequisite source closure
  is the only stage that may authorize Stage 03 via GAP_VERIFIED
```

A source-resolvable unknown is blocking before technical design when an authoritative design question requires current-source truth to answer it materially. Knowing that a feature is missing does not make invocation points, result representation, client-IP propagation, authentication distinctions, timeout distinctions, or integration-point topology safe to invent later.

Fresh-run artifacts and workflow state must be run-scoped and physically present at workflow-declared paths. A downstream stage may not be satisfied by a stale shared artifact or an undeclared summary file.

When an operator requests an intermediate stop, use explicit inclusive `stop_after_step` semantics. The requested step must execute and persist its gate before the workflow stops.


## Current-State Consumer Model Quality

Full reverse engineering must convert verified evidence into a consumer-usable current-state technical model.

Required full-baseline outputs:

```text
CURRENT_STATE_TDD.md
5 evidence-linked Mermaid diagram artifacts
component/runtime-flow/integration/configuration/persistence-state model artifacts
separate readiness audit
```

Readiness requires both evidence correctness and model usability. A fact inventory or adversarial audit report does not substitute for a Current-State TDD.

Mandatory diagram families:

```text
system context
component architecture
primary runtime sequence
integration boundaries
state/persistence/lifecycle
```

Run `python .ai-engineering/tools/validate-reverse-engineering-quality.py --artifact-root docs/reverse-engineering` before declaring the full baseline ready.
