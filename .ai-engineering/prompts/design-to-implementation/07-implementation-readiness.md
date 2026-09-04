# Stage 07 — Implementation Readiness Certification

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Inputs:
- requirement
- current-state analysis
- gap analysis
- verified TDD + verification
- artifact registry
- detailed designs + verification
- WBS + verification
- test design
- open-question state
- current repository for critical reverification

Run `/implementation-readiness-certification`.

Do not generate new design or new WBS tasks in this stage.
Certify readiness and identify blockers.

Write:
`{{implementation_readiness_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: implementation_readiness
  status: IMPLEMENTATION_READY | IMPLEMENTATION_READY_WITH_EXTERNAL_BLOCKERS | NOT_READY_DESIGN_GAPS | NOT_READY_WBS_GAPS | NOT_READY_SOURCE_GAPS
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{implementation_readiness_artifact}}"
  next_recommended: null
```