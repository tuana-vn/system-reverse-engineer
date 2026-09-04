# Targeted Source Analysis

## Inputs

- scope: `{{scope}}`
- exact analysis question: `{{analysis_question}}`
- optional source anchor: `{{source_anchor}}`
- optional requirement: `{{requirement_path}}`
- analysis mode: `{{analysis_mode}}`
- current repository

## Goal

Answer one concrete source-backed technical question without automatically running the
entire reverse-engineering baseline workflow.

Use the current repository as the authority for CURRENT behavior.

Mandatory:
- define the exact scope
- trace caller/callee/runtime flow where applicable
- trace field/data provenance where applicable
- perform Boundary → Exposure Closure where an integration boundary is involved
- inspect runtime/config binding where it changes the answer
- search counterexamples before broad conclusions
- distinguish CURRENT / PROPOSED / UNKNOWN
- do not turn a targeted analysis into a design proposal

Use additional targeted skills only when the evidence requires them:
- `/configuration-source-trace`
- `/runtime-binding-verification`
- `/integration-selection-analysis`
- `/persistence-schema-reverse-engineering`

Write:
`{{artifact_root}}/analysis/{{scope_slug}}_targeted_analysis.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: targeted-source-analysis
  step: targeted_analysis
  status: TARGETED_ANALYSIS_COMPLETE | TARGETED_ANALYSIS_PARTIAL | TARGETED_ANALYSIS_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/analysis/{{scope_slug}}_targeted_analysis.md"
  next_recommended: null | resolve_unknowns
```
