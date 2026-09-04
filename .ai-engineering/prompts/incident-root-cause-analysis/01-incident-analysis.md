# Incident Root Cause Analysis

Inputs:
- incident evidence/input: `{{incident_input}}`
- scope: `{{scope}}`
- current repository/runtime/config evidence

Run `/incident-root-cause-analysis`.

Use runtime-flow and claim-verification skills when code-path proof is required.

Mandatory separation:
- OBSERVED FACT
- SOURCE-BACKED MECHANISM
- CANDIDATE CAUSE
- DISCONFIRMING EVIDENCE
- UNKNOWN / MISSING EVIDENCE

Do not convert correlation into root cause.

Write:
`{{artifact_root}}/incidents/{{scope_slug}}_root_cause_analysis.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: incident-root-cause-analysis
  step: incident_analysis
  status: RCA_COMPLETE | RCA_PARTIAL_EVIDENCE | RCA_SOURCE_GAPS
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/incidents/{{scope_slug}}_root_cause_analysis.md"
  next_recommended: null | resolve_rca_unknowns
```
