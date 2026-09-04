# Workflow Matrix — System Reverse Engineer 4.0

| Workflow | Use Case | Use When | Required Inputs | Major Outputs | Success Gate |
|---|---|---|---|---|---|
| `full-reverse-engineering.yaml` | UC-01 | Missing/untrusted baseline | none | `CURRENT_STATE_TDD.md` + diagrams/models + readiness audit | `BASELINE_READY*` |
| `targeted-source-analysis.yaml` | UC-03/13/14/15/16 | One exact technical question | scope, scope_slug, analysis_question | targeted current-state analysis | `TARGETED_ANALYSIS_COMPLETE` |
| `patch-impact-to-tests.yaml` | UC-04 | Patch/diff exists | patch_path, scope, scope_slug; optional requirement | impact/compliance/test artifacts | `TEST_DESIGN_COMPLETE` |
| `requirement-to-design.yaml` | UC-05/06 | Requirement needs current-state/gap/TDD | requirement_path, scope, scope_slug | current-state, gap, TDD, test design | `workflow complete` |
| `design-to-implementation.yaml` | UC-07 | Verified TDD exists | requirement/current/gap/TDD paths + scope | DD registry/details, WBS, readiness | `IMPLEMENTATION_READY*` |
| `requirement-to-implementation-plan.yaml` | UC-08 | Need end-to-end planning | requirement_path, scope, scope_slug | full analysis/design/WBS chain | `IMPLEMENTATION_READY*` |
| `claim-justification.yaml` | UC-09 | Exact claim must be proven/narrowed | claim, scope, scope_slug | claim justification | `claim verdict` |
| `architecture-drift-rebaseline.yaml` | UC-10 | Baseline may be stale after source change | scope, scope_slug; optional change_range | drift/rebaseline report | `REBASELINE_COMPLETE` |
| `incident-root-cause-analysis.yaml` | UC-11 | Incident/log/runtime symptom | incident_input, scope, scope_slug | RCA artifact | `RCA_COMPLETE/PARTIAL` |
| `observability-traceability-analysis.yaml` | UC-12 | Audit/log/metric/trace question | analysis_question, scope, scope_slug | observability trace | `OBSERVABILITY_TRACE_COMPLETE` |

| `post-readiness-audit.yaml` | UC-17 | Re-audit an existing IMPLEMENTATION_READY package | source_run_id, source_workflow_state, requirement_path, scope, scope_slug | adversarial post-readiness audit | `POST_READINESS_AUDIT_PASS*` |
