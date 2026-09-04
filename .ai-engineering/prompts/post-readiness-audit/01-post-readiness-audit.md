# 4.0 Fresh Execution Contract

Agent package version: `{{agent_package_version}}`
Run ID: `{{run_id}}`
Execution mode: `{{execution_mode}}`

This workflow defaults to:

```yaml
execution_mode: fresh
ignore_previous_completion: true
```

A prior audit completion/verdict MUST NOT satisfy this invocation. Re-read current workflow,
prompt, skill, state, artifacts, and repository evidence from disk.

# Post-Readiness Adversarial Audit

## Inputs

- scope: `{{scope}}`
- scope slug: `{{scope_slug}}`
- source workflow run ID: `{{source_run_id}}`
- persisted workflow state: `{{source_workflow_state}}`
- source run manifest: `{{source_run_manifest}}`
- authoritative requirement: `{{requirement_path}}`
- current repository
- prior generated artifacts resolved from workflow state/gates

Run:

```text
/post-readiness-adversarial-audit
```

## Goal

Independently challenge the prior `IMPLEMENTATION_READY` result.

Do NOT:
- modify TDD/DD/WBS/readiness artifacts
- trust previous readiness prose
- guess missing artifact paths
- ask the user to manually pick WBS IDs
- skip source reverification for high-impact sampled claims
- treat Artifact ID existence as semantic proof
- relabel an Artifact ID from nearby TDD/DD prose
- claim ALL WBS tasks passed when only a sample was deeply traced

The skill must resolve actual artifact paths from persisted workflow state and recorded stage gates.

## Required Audit Areas

```text
1. workflow/gate integrity
2. exhaustive WBS ↔ artifact semantic identity audit
3. deterministic deep WBS backward-trace sample
4. proposed static architecture consistency
5. MUST-NOT / negative-rule coverage
6. Boundary → Exposure re-audit for every materially changed integration boundary
7. WBS missing-work recheck
8. current-source anchor health
9. cross-section canonical Artifact ID identity consistency
10. quantitative scorecard
```

Write:

`{{post_readiness_audit_artifact}}`

End with exactly:

```yaml
WORKFLOW_GATE:
  workflow: post-readiness-audit
  step: post_readiness_audit
  status: POST_READINESS_AUDIT_PASS | POST_READINESS_AUDIT_PASS_WITH_WARNINGS | POST_READINESS_AUDIT_FAIL_SOURCE_GAPS | POST_READINESS_AUDIT_FAIL_DESIGN_GAPS | POST_READINESS_AUDIT_FAIL_WBS_GAPS | POST_READINESS_AUDIT_FAIL_WORKFLOW_INTEGRITY | POST_AUDIT_INPUT_NOT_RESOLVED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{post_readiness_audit_artifact}}"
  next_recommended: null
```