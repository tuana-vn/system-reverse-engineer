# Verify Drift and Rebaseline

Inputs:
- drift report
- promoted baseline
- current repository
- evidence/open-question artifacts

Run:
- `/adversarial-baseline-audit`
- `/reverse-engineering-coverage-audit`
- `/baseline-source-of-truth-maintenance`

Rules:
- current source/runtime evidence wins over generated baseline
- search counterexamples before broad replacement claims
- do not promote unresolved HIGH/CRITICAL source-resolvable claims
- preserve evidence history
- do not promote requirements, proposals, unmerged patches, or hypotheses as current behavior

Write:
`{{artifact_root}}/reviews/{{scope_slug}}_rebaseline_report.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: architecture-drift-rebaseline
  step: verify_drift
  status: REBASELINE_COMPLETE | REBASELINE_NOT_READY | REBASELINE_BLOCKED_EXTERNAL
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/reviews/{{scope_slug}}_rebaseline_report.md"
  next_recommended: null | resolve_drift_unknowns
```
