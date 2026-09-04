# Observability / Traceability Analysis

Inputs:
- question: `{{analysis_question}}`
- scope: `{{scope}}`
- optional requirement: `{{requirement_path}}`
- current repository/runtime/config evidence

Run `/observability-traceability-analysis`.

Trace where applicable:

```text
trigger
→ request/runtime context
→ decision whether to emit
→ context/data provenance
→ logging/audit/metric/trace invocation
→ sink/boundary
→ observable record/result
```

Also prove:
- excluded paths
- background/internal vs external origin when relevant
- error/success distinctions
- failure behavior of instrumentation
- sensitive-data handling when relevant

Do not assume one common instrumentation wrapper unless source proves it.

Write:
`{{artifact_root}}/analysis/{{scope_slug}}_observability_trace.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: observability-traceability-analysis
  step: trace_observability
  status: OBSERVABILITY_TRACE_COMPLETE | OBSERVABILITY_TRACE_PARTIAL | OBSERVABILITY_TRACE_BLOCKED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/analysis/{{scope_slug}}_observability_trace.md"
  next_recommended: null | resolve_observability_unknowns
```
