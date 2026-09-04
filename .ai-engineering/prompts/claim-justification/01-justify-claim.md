# High-Impact Claim Justification

Inputs:
- exact claim: `{{claim}}`
- scope: `{{scope}}`
- current repository
- requirement/specification if supplied: `{{requirement_path}}`

Run `/claim-verification-and-promotion`.

Mandatory proof:
- exact semantic wording
- scope matrix
- current-source evidence
- runtime wiring
- field/data provenance if data/output-related
- Boundary → Exposure Closure if reachability-related
- counterexample search
- narrower replacement claim when the exact wording cannot be proven

Write:
`{{artifact_root}}/reviews/{{scope_slug}}_claim_justification.md`

End with:

```yaml
WORKFLOW_GATE:
  workflow: claim-justification
  step: justify_claim
  status: CLAIM_PROVEN | CLAIM_PARTIALLY_PROVEN | CLAIM_NOT_PROVEN | CLAIM_CONTRADICTED | CLAIM_SOURCE_NOT_RESOLVED
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: "{{artifact_root}}/reviews/{{scope_slug}}_claim_justification.md"
  next_recommended: null
```
