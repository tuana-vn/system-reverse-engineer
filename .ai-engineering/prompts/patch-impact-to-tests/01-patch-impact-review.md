# Patch Impact Review Stage

Inputs:
- patch/diff: `{{patch_path}}`
- requirement/spec if supplied: `{{requirement_path}}`
- scope: `{{scope}}`
- current repository and promoted baseline

Run `/patch-impact-review`.

Mandatory:
- changed code → runtime impact
- downstream boundary → ALL exposure closure
- request/output/data provenance
- before-vs-after behavior
- compatibility/regression risk
- evidence-backed test viewpoints
- no representative-endpoint shortcut

Write:
`{{artifact_root}}/reviews/{{scope_slug}}_patch_impact.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: patch-impact-to-tests
  step: patch_impact_review
  status: PATCH_REVIEW_COMPLETE | PATCH_REVIEW_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/reviews/{{scope_slug}}_patch_impact.md"
  next_recommended: requirement_compliance | regression_test_design | resolve_patch_unknowns
```
