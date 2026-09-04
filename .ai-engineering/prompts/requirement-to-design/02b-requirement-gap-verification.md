# Stage 02B — Independent Requirement-Gap Verification

## Inputs

- authoritative requirement: `{{requirement_path}}`
- current-state artifact: `{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`
- requirement-gap artifact: `{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md`
- current repository when source re-check is required

## Independence Rule

Do not trust the generator's `DESIGN_READY`, summary, counts, IDs, self-checks, source-readiness labels, or field obligations. Recompute independently from the authoritative requirement, Stage 01 evidence, and the primary compliance matrix.

## Mandatory Verification

1. Requirement identity stability
   - Reconstruct canonical scenario and constraint rows directly from the authoritative requirement.
   - Verify Stage 01/02 IDs and semantics exactly match.
   - Recompute `scenario_rule_count`, `constraint_rule_count`, and `canonical_rule_count` from actual rows.
2. Requirement fidelity
   - Search Stage 02 for mandatory fields/scenarios/acceptance criteria not explicit in the requirement.
   - Treat source-available fields as CURRENT availability only.
   - Any useful future addition must be clearly `PROPOSED_DESIGN`, not requirement text.
3. Aggregate consistency
   - Recompute compliance counts from the detailed matrix.
   - Executive summary and `GAP_INTEGRITY` must match.
4. Stage 01 domain discipline
   - Stage 01 must not classify requirements as `IMPLEMENTATION_GAP`, `NO_GAP`, or `DESIGN_GAP`.
   - Requirement statements must not be relabeled as CURRENT source proof.
5. Source readiness for Stage 03
   - Re-read every authoritative Required Design Question.
   - For each unresolved source Q-ID, ask whether Stage 03 can answer the design question correctly without inventing current behavior.
   - If not, classify it `DESIGN_PREREQUISITE_SOURCE_GAP` and block progression.
   - Do not defer source mapping that the TDD itself is explicitly required to answer.
6. Transition integrity
   - Stage 02 `DESIGN_READY` must point to `requirement_gap_verification`, never directly to `technical_design`.
   - Stage 02B is the only stage that may authorize transition to `technical_design` via `GAP_VERIFIED`.

Do not call a semantic Python validator. The verifier owns this reasoning.

## Output

Write:

`{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap_verification.md`

Include a concise finding table with evidence and responsible upstream stage for every contradiction.

End with exactly one:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: requirement_gap_verification
  status: GAP_VERIFIED | GAP_CONTRADICTED | GAP_BLOCKED_SOURCE_GAPS
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  requirement_id_collisions: <integer>
  requirement_semantic_mismatches: <integer>
  summary_matrix_mismatches: <integer>
  invented_requirement_obligations: <integer>
  stage_transition_contradictions: <integer>
  design_prerequisite_source_gaps: <integer>
  artifact: "{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap_verification.md"
  next_recommended: technical_design | revise_requirement_gap | resolve_gap_unknowns
```

`GAP_VERIFIED` requires all semantic defect counts and `design_prerequisite_source_gaps` to be 0.
