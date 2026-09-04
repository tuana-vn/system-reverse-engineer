# Resolve Workflow-Blocking High-Impact Unknowns

Use `/resolve-high-impact-unknowns`.

Inputs:

- blocking artifact: `{{blocking_artifact}}`
- blocking Q-IDs: `{{blocking_qids}}`
- current repository

Resolve ONLY the source-resolvable HIGH/CRITICAL questions blocking the active workflow step.

For each question:
- search from multiple anchors
- close field/data provenance when applicable
- close Boundary → Exposure paths when applicable
- search counterexamples
- record exact source evidence
- do not propose downstream design merely to avoid the unknown

Write/update the normal high-impact unknown closure artifact and workflow state.

Return control to:

`{{retry_step}}`


## 4.0 Source-Fact Boundary

A resolved source fact closes only the factual question that was searched. Do not promote a specific
future mechanism, heuristic, parameter, class, or policy to VERIFIED merely because CURRENT source
proves the existing mechanism is absent. Any implementation recommendation must be labeled PROPOSED
and deferred to the appropriate design stage.
