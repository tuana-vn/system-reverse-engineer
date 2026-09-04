# Stage 04 — Verify One Artifact Detailed Design

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`


Artifact:
- ID: `{{artifact_id}}`
- design: `{{artifact_root}}/design/details/{{artifact_id}}-{{artifact_slug}}.md`

Inputs:
- requirement
- gap analysis
- verified TDD
- TDD verification
- artifact registry
- current repository

Run `/detailed-design-verification`.

Do not revise the detailed design while verifying.
Record required corrections separately.

MANDATORY:
- inspect every architecture/static-structure view in the DD;
- independently classify nodes/relationships as CURRENT / PROPOSED / UNKNOWN;
- a CURRENT-labeled view containing PROPOSED elements cannot receive `DD_VERIFIED`;
- explicitly report `CURRENT_PROPOSED_ARCHITECTURE_CONTAMINATION` when applicable;
- do not certify `Risk: LOW`, `Regression Risk: NONE`, `Confidence: HIGH`, or similar labels unless
  measurable criteria and closure evidence are present;
- explicitly report `UNSUPPORTED_QUALITATIVE_RISK_CLAIM` when applicable.

Write:
`{{artifact_root}}/design/verification/{{artifact_id}}-verification.md`

Update the artifact registry DD verification status.

End with:

```yaml
WORKFLOW_GATE:
  workflow: design-to-implementation
  step: detailed_design_verification
  artifact_id: "{{artifact_id}}"
  status: DD_VERIFIED | DD_PARTIALLY_VERIFIED | DD_CONTRADICTED_BY_SOURCE | DD_BLOCKED_SOURCE_GAP
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/design/verification/{{artifact_id}}-verification.md"
  next_recommended: next_artifact | revise_current_dd | resolve_dd_unknowns
```
