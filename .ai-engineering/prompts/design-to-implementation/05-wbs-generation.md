# Stage 05 — Generate Implementation WBS

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

Precondition:
ALL implementation-required design artifacts are `DD_VERIFIED`.

Inputs:
- requirement
- gap analysis
- verified TDD
- design artifact registry
- all verified detailed designs
- all DD verification reports
- current repository
- existing contract/regression test design if available

Run `/wbs-generation`.

Do NOT estimate effort.

Before declaring WBS ready, verify that every task's primary deliverable is actually owned by its referenced design artifact according to the registry / VERIFIED DD. Do not use a nearby TDD/DD mention as semantic ownership evidence.

Write:
`{{wbs_artifact}}`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: wbs_generation
  status: WBS_READY_FOR_VERIFICATION | WBS_BLOCKED_DESIGN_GAP | WBS_BLOCKED_SOURCE_GAP
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{wbs_artifact}}"
  next_recommended: wbs_verification | return_to_dd | resolve_wbs_unknowns
```