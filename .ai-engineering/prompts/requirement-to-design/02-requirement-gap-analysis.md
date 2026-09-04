# Stage 02 — Requirement Gap Analysis

## Inputs

- authoritative requirement: `{{requirement_path}}`
- current-state artifact: `{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`
- current repository for targeted reverification
- scope: `{{scope}}`

## Goal

Determine requirement compliance, verified gaps/non-gaps, design constraints, and whether unresolved source questions block **technical design**.

Run `/requirement-compliance-review`.

Do NOT produce the final technical design.

## Canonical rules

- Copy the Stage 01 `REQUIREMENT_IDENTITY` ledger verbatim, including all three counts.
- Requirement IDs are immutable within the run.
- The detailed compliance matrix is the single source of truth for aggregate metrics.
- Every canonical rule gets exactly one primary verdict: `IMPLEMENTATION_GAP`, `NO_GAP`, `DESIGN_GAP`, or blocker state.
- Preserve explicit MUST-NOT rules and design constraints.
- Do not add mandatory fields/scenarios/acceptance criteria/obligations absent from the authoritative requirement.
- Source-discovered availability is CURRENT evidence, not a new requirement.
- For every field/data row, distinguish:
  - `EXPLICIT_REQUIREMENT` — authoritative requirement explicitly mandates it;
  - `SOURCE_AVAILABLE` — source contains it but requirement does not mandate it;
  - `PROPOSED_DESIGN` — a future design choice, not a requirement.
- Never write `MUST INCLUDE`, `MUST CAPTURE`, or equivalent for session ID, user ID, timestamp, response body, token, logout cause, or any other field unless the authoritative requirement explicitly says so.

## Source-readiness rule before Technical Design

Stage 02 is the owner of deciding whether unresolved source questions may reach Stage 03.

A source-resolvable unknown is a **DESIGN_PREREQUISITE_SOURCE_GAP** when the authoritative TDD/design questions require source truth to answer it materially, including questions such as:
- where a current call/invocation occurs;
- where a result becomes known and how it is represented;
- how current request/client-IP context is available or propagated;
- how current explicit-vs-timeout deletion is distinguished;
- how current auth success/failure is represented;
- how current internal/background operations are distinguished;
- whether a common integration point actually exists.

Such an unknown MUST NOT be relabeled `NON_BLOCKING_DEFERRED` merely because the existence of the high-level gap is already known.

If any unresolved source-resolvable unknown is materially required to answer an authoritative design question, emit `DESIGN_NOT_READY_SOURCE_GAPS` and route to `resolve_gap_unknowns` before Stage 02B/Stage 03.

Only source questions that no material Stage-03 decision depends on may be `NON_BLOCKING_DEFERRED`.

## Aggregate discipline

Before writing any summary:
1. freeze the canonical compliance matrix;
2. derive all counts from it;
3. derive scenario/constraint/canonical counts from the copied identity ledger;
4. do not independently hand-author totals.

Do not state `all requirements have gaps` unless every canonical rule row is non-`NO_GAP`.

## Output

Write:

`{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md`

Include:
- copied requirement identity ledger
- requirement compliance matrix
- observable behavior matrix where applicable
- field/data provenance matrix with requirement-vs-source-vs-proposed classification
- verified gap register
- explicit non-gaps / preserved behavior
- design constraints
- source-readiness table mapping unresolved Q-IDs to Stage-03 design questions they block, if any

Emit exactly once:

```yaml
GAP_INTEGRITY:
  scenario_rule_count: <integer from ledger>
  constraint_rule_count: <integer from ledger>
  canonical_rule_count: <integer from ledger>
  matrix_rule_count: <integer>
  requirement_id_collisions: <integer>
  requirement_semantic_mismatches: <integer>
  summary_implementation_gap_count: <integer>
  matrix_implementation_gap_count: <integer>
  summary_no_gap_count: <integer>
  matrix_no_gap_count: <integer>
  summary_design_gap_count: <integer>
  matrix_design_gap_count: <integer>
  invented_requirement_obligations: <integer>
  design_prerequisite_source_gaps: <integer>
```

Before `DESIGN_READY`, all identity/summary/invention counts must be clean and `design_prerequisite_source_gaps` must be 0.

IMPORTANT transition contract:
- `DESIGN_READY` means **ready for independent requirement-gap verification**, NOT ready to skip directly to technical design.
- The next stage after `DESIGN_READY` is `requirement_gap_verification`.
- Do not write `proceed to technical_design` until Stage 02B returns `GAP_VERIFIED`.

End with:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: requirement_gap_analysis
  status: DESIGN_READY | DESIGN_READY_WITH_EXTERNAL_BLOCKERS | DESIGN_NOT_READY_SOURCE_GAPS
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md"
  next_recommended: requirement_gap_verification | resolve_gap_unknowns
```
