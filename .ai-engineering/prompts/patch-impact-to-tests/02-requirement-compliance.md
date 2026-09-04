# Patch Requirement Compliance Stage

Inputs:
- requirement: `{{requirement_path}}`
- patch impact: `{{artifact_root}}/reviews/{{scope_slug}}_patch_impact.md`
- current repository

Run `/requirement-compliance-review`.

Do not treat patch implementation shape as requirement semantics.
Preserve scope isolation and provenance gates.

Write:
`{{artifact_root}}/reviews/{{scope_slug}}_patch_compliance.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: patch-impact-to-tests
  step: requirement_compliance
  status: COMPLIANCE_REVIEW_COMPLETE | COMPLIANCE_REVIEW_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/reviews/{{scope_slug}}_patch_compliance.md"
  next_recommended: regression_test_design | resolve_compliance_unknowns
```
