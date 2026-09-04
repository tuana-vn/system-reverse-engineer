# Stage 01 — Verify Technical Design

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Inputs:
- requirement: `{{requirement_path}}`
- current-state analysis: `{{current_state_artifact}}`
- gap analysis: `{{gap_artifact}}`
- TDD: `{{tdd_path}}`
- current repository
- scope: `{{scope}}`

Run `/technical-design-verification`.

Do not improve or rewrite the TDD in this stage.
Verify it.

Write:
`{{tdd_verification_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: tdd_verification
  status: TDD_VERIFIED | TDD_PARTIALLY_VERIFIED | TDD_CONTRADICTED | TDD_BLOCKED_SOURCE_GAPS | TDD_INCOMPLETE_ARCHITECTURE | TDD_INCOMPLETE_PROPOSED_UNIT_OWNERSHIP
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{tdd_verification_artifact}}"
  next_recommended: design_artifact_decomposition | resolve_tdd_unknowns | revise_tdd
```