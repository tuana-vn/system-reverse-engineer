# Use Case → Workflow → Prompt → Skill → Artifact Matrix

This is the navigation/source-of-truth matrix for operating the package.

| Use Case | Workflow | Prompt(s) | Main Skills | Output/Gate |
|---|---|---|---|---|
| UC-01 Full baseline | `full-reverse-engineering.yaml` | inline workflow instruction + skill-internal stages | `full-reverse-engineering`, `architecture-reconstruction-and-diagrams`, `current-state-tdd-synthesis` plus source/evidence skills | `CURRENT_STATE_TDD.md` + diagrams/models / `BASELINE_READY*` |
| UC-03 Targeted analysis | `targeted-source-analysis.yaml` | `.ai-engineering/prompts/targeted-source-analysis/01-targeted-analysis.md` | runtime flow + claim verification; add config/binding/integration/persistence as needed | targeted analysis |
| UC-04 Patch impact | `patch-impact-to-tests.yaml` | 3 patch prompts | patch impact, compliance optional, regression/contract tests | impact/compliance/test design |
| UC-05/06 Requirement analysis/design | `requirement-to-design.yaml` | 4 requirement prompts | runtime flow, compliance, claim verify, TDD, tests | current state → gap → TDD → tests |
| UC-07 Design to implementation | `design-to-implementation.yaml` | 7 design/WBS prompts | TDD verify, decomposition, DD, DD verify, WBS, WBS verify, readiness | implementation readiness |
| UC-08 End-to-end implementation plan | `requirement-to-implementation-plan.yaml` | composes UC-06 + UC-07 | child-workflow skills | full traceability chain |
| UC-09 Claim proof | `claim-justification.yaml` | `.ai-engineering/prompts/claim-justification/01-justify-claim.md` | claim verification | exact/narrowed claim verdict |
| UC-10 Drift/rebaseline | `architecture-drift-rebaseline.yaml` | drift + rebaseline prompts | drift detection, adversarial/coverage audit, baseline maintenance | verified rebaseline |
| UC-11 RCA | `incident-root-cause-analysis.yaml` | incident analysis prompt | RCA, runtime flow, claim verification | evidence-backed RCA |
| UC-12 Observability | `observability-traceability-analysis.yaml` | observability prompt | observability trace, runtime flow, claim verification | emission/provenance analysis |

## Reading Direction

For a human:

```text
Use Case Catalog
→ choose workflow
→ copy only workflow invocation + inputs
```

For the agent:

```text
workflow
→ load prompt for active stage
→ apply named skills
→ write artifact
→ validate WORKFLOW_GATE
→ transition
```

Do not manually pick a long list of skills if a workflow already declares them.

| UC-17 Post-readiness adversarial audit | `.ai-engineering/workflows/post-readiness-audit.yaml` | `.ai-engineering/prompts/post-readiness-audit/01-post-readiness-audit.md` | `post-readiness-adversarial-audit` | audited handoff / `POST_READINESS_AUDIT_PASS*` |
