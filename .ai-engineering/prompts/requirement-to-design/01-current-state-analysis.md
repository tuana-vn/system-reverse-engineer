# Stage 01 — Current-State Source Analysis

## Inputs

- authoritative requirement: `{{requirement_path}}`
- analysis scope: `{{scope}}`
- current repository
- promoted baseline only as supporting context

## Goal

Reconstruct CURRENT behavior relevant to the requirement. This stage is analysis only.

Do NOT:
- propose a solution
- design new classes/interfaces
- modify production code
- update canonical baseline from the requirement
- fill source gaps with plausible architecture
- classify requirement compliance as `IMPLEMENTATION_GAP`, `NO_GAP`, or `DESIGN_GAP`; those labels belong to Stage 02

Use `/runtime-flow-analysis`, `/claim-verification-and-promotion`, and other targeted source-tracing skills only as required by the actual repository.

## Mandatory analysis

1. Normalize the authoritative requirement into a canonical requirement identity ledger and scope matrix.
   - Assign deterministic IDs once, in authoritative source order.
   - Use separate namespaces for scenario rules and design constraints, e.g. `SCN-001...` and `CON-001...`.
   - One ID MUST map to exactly one semantic rule for the entire run.
   - Do not collapse distinct MUST LOG decision-matrix rows when materially different operations are listed.
   - Preserve authoritative wording/meaning; IDs are labels, not reinterpretations.
   - Count the ledger mechanically from the rows actually emitted. Never hand-type a total that disagrees with the ledger.
2. Identify relevant external entry points / operations.
3. Trace representative and materially distinct current runtime paths.
4. For important downstream boundaries, perform Boundary → Exposure Closure.
5. For externally meaningful fields/data/context, prove field/data provenance.
6. Identify current configuration/routing/binding that changes relevant behavior.
7. Search counterexamples and sibling operations before broad claims.
8. Record source-resolvable unknowns explicitly with impact and the next stage that actually needs them.
9. Before the workflow gate, perform stage-transition integrity validation from one `STAGE_INTEGRITY` decision.

## Current-State Discipline

- Describe only `CURRENT`, `UNKNOWN`, and clearly labeled `REQUIREMENT-CONFIRMED FUTURE CONSTRAINT` facts.
- Requirement statements are scope/intended behavior, not proof of current source implementation.
- Do not say that a requirement row is an implementation gap or no-gap in Stage 01.
- Do not infer that an ESM-side symptom proves how PF REST internally captures or propagates client IP.
- Do not prescribe future fields, heuristics, classes, query parameters, constructor changes, logging formats, or integration points.
- If only non-blocking unknowns remain for **gap identification**, Stage 01 may proceed, but retain them as unresolved inputs for Stage 02 to classify as design prerequisites or non-blocking deferred work.

## Output

Write:

`{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`

Emit these blocks exactly once before the gate:

```yaml
REQUIREMENT_IDENTITY:
  source: "{{requirement_path}}"
  scenario_rule_count: <integer derived from emitted SCN rows>
  constraint_rule_count: <integer derived from emitted CON rows>
  canonical_rule_count: <scenario_rule_count + constraint_rule_count>
  rules:
    - id: <SCN-xxx or CON-xxx>
      category: <MUST_LOG | MUST_NOT_LOG | DESIGN_CONSTRAINT>
      semantic_key: <stable_short_key>
      semantic_rule: <authoritative meaning, no design invention>
```

```yaml
STAGE_INTEGRITY:
  blocking_source_unknowns: <integer>
  nonblocking_source_unknowns: <integer>
  progression_allowed: <true|false>
  narrative_requires_resolution_before_next_stage: <true|false>
```

`progression_allowed=true` requires `narrative_requires_resolution_before_next_stage=false`.

Use one transition form, matching `STAGE_INTEGRITY` exactly:

- If true: `Remaining source unknowns are retained for Stage 02 classification. They do not block requirement_gap_analysis itself.`
- If false: `Source tracing is required before requirement_gap_analysis; remain PARTIAL/BLOCKED and resolve current-state unknowns first.`

End with exactly one:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: current_state_analysis
  status: CURRENT_STATE_ANALYSIS_COMPLETE | CURRENT_STATE_ANALYSIS_PARTIAL | CURRENT_STATE_ANALYSIS_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/analysis/{{scope_slug}}_current_state.md"
  next_recommended: requirement_gap_analysis | resolve_current_state_unknowns
```
