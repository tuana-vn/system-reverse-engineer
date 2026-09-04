# Stage 02B — Independently Verify Design Artifact Decomposition

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Inputs:
- requirement: `{{requirement_path}}`
- verified gap analysis: `{{gap_artifact}}`
- verified TDD: `{{tdd_path}}`
- TDD verification: `{{tdd_verification_artifact}}`
- candidate registry: `{{design_registry_artifact}}`
- current repository

Run `/design-artifact-decomposition-verification`.

IMPORTANT:
- independently enumerate PROPOSED implementation-significant units from the TDD
- do not derive the inventory from the registry artifact rows
- do not trust `ARTIFACT_REGISTRY_READY`
- compare the independent unit inventory against explicit registry ownership
- a mention/reference/import/throws/@see is not ownership
- do not modify the registry while verifying

Write:
`{{design_registry_verification_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: design_artifact_decomposition_verification
  status: ARTIFACT_DECOMPOSITION_VERIFIED | ARTIFACT_DECOMPOSITION_VERIFICATION_FAILED | ARTIFACT_DECOMPOSITION_VERIFICATION_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{design_registry_verification_artifact}}"
  next_recommended: artifact_detailed_design_loop | revise_tdd | resolve_registry_unknowns
```
