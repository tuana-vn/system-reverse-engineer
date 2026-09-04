# Patch Regression Test Design Stage

Inputs:
- patch impact artifact
- compliance artifact if requirement exists
- current source/tests

Run `/regression-test-design`.
Use `/contract-impact-test-design` when an externally visible contract is impacted.

Write:
`{{artifact_root}}/test-design/{{scope_slug}}_patch_regression.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: patch-impact-to-tests
  step: regression_test_design
  status: TEST_DESIGN_COMPLETE | TEST_DESIGN_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/test-design/{{scope_slug}}_patch_regression.md"
  next_recommended: null
```
