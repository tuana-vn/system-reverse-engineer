# Stage 06 — Verify Implementation WBS

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Inputs:
- requirement
- gap analysis
- verified TDD
- artifact registry
- all DD_VERIFIED designs
- WBS: `{{wbs_artifact}}`
- current repository
- test design

Run `/wbs-verification`.

Actively search for missing work.
Do not only review tasks that already exist.

Exhaustively verify semantic identity for EVERY WBS task:

```text
task primary deliverable
↔ referenced Artifact ID
↔ canonical registry responsibility
↔ VERIFIED DD owned implementation unit
```

An existing Artifact ID alone is not enough. Any `WBS_ARTIFACT_SEMANTIC_MISMATCH` blocks `WBS_VERIFIED`.

Write:
`{{wbs_verification_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: wbs_verification
  status: WBS_VERIFIED | WBS_PARTIALLY_VERIFIED | WBS_INCOMPLETE | WBS_BLOCKED_SOURCE_GAP
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{wbs_verification_artifact}}"
  next_recommended: implementation_readiness | revise_wbs | resolve_wbs_unknowns
```