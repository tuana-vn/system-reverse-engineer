# Stage 03 — Detailed Design for One Artifact

Current artifact:
- Artifact ID: `{{artifact_id}}`
- Artifact name: `{{artifact_name}}`
- Artifact slug: `{{artifact_slug}}`

Inputs:
- registry: `{{design_registry_artifact}}`
- requirement: `{{requirement_path}}`
- gap analysis: `{{gap_artifact}}`
- TDD: `{{tdd_path}}`
- TDD verification
- current repository

Run `/artifact-detailed-design`.

IMPORTANT:
- design exactly ONE artifact
- reverify current source anchors
- do not copy an assumed pattern from another artifact
- if a dependency blocks this artifact, stop with DD_BLOCKED_DEPENDENCY
- existing/proposed/unknown must be separated explicitly

Write:
`{{artifact_root}}/design/details/{{artifact_id}}-{{artifact_slug}}.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: artifact_detailed_design
  artifact_id: "{{artifact_id}}"
  status: DD_READY_FOR_VERIFICATION | DD_BLOCKED_SOURCE_GAP | DD_BLOCKED_DEPENDENCY
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/design/details/{{artifact_id}}-{{artifact_slug}}.md"
  next_recommended: detailed_design_verification | resolve_dd_unknowns
```
