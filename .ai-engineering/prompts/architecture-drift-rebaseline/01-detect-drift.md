# Detect Architecture Drift

Inputs:
- scope: `{{scope}}`
- optional change range: `{{change_range}}`
- promoted baseline
- current repository

Run `/architecture-drift-detection`.

Goal:
identify source-backed differences between current source/runtime wiring and the promoted baseline.

Do not update the baseline in this stage.

Write:
`{{artifact_root}}/reviews/{{scope_slug}}_architecture_drift.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: architecture-drift-rebaseline
  step: detect_drift
  status: DRIFT_NOT_FOUND | DRIFT_FOUND_VERIFICATION_REQUIRED | DRIFT_ANALYSIS_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/reviews/{{scope_slug}}_architecture_drift.md"
  next_recommended: null | verify_drift | resolve_drift_unknowns
```
