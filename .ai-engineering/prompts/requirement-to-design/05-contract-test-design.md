# Stage 05 — Contract / Regression Test Design

## Inputs

- requirement: `{{requirement_path}}`
- current-state analysis: `{{artifact_root}}/analysis/{{scope_slug}}_current_state.md`
- gap analysis: `{{artifact_root}}/analysis/{{scope_slug}}_requirement_gap.md`
- TDD: `{{artifact_root}}/proposals/{{scope_slug}}_tdd.md`
- current source/tests

Run `/contract-impact-test-design` and `/regression-test-design` as applicable.

## Goal

Produce source/requirement-backed verification for the proposed change.

## Oracle rule

Expected behavior must trace as:

```text
requirement / preserved verified rule
→ trigger/input condition
→ expected runtime/downstream behavior
→ expected data provenance/state
→ observable result
```

Do not use current implementation alone as the oracle for new behavior.

## Output

Write:

`{{artifact_root}}/test-design/{{scope_slug}}_test_design.md`

and when a matrix is appropriate:

`{{artifact_root}}/test-design/{{scope_slug}}_test_matrix.csv`

End the Markdown artifact with:

```yaml
WORKFLOW_GATE:
  workflow: requirement-to-design
  step: contract_test_design
  status: TEST_DESIGN_COMPLETE | TEST_DESIGN_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/test-design/{{scope_slug}}_test_design.md"
  next_recommended: null
```
