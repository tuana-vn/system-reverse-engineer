---
name: run-engineering-workflow
description: Execute a declarative System Reverse Engineer workflow as a guarded state machine. In Autopilot, execute stages sequentially within the same user task until the workflow reaches a terminal state, while validating and persisting each stage independently.
argument-hint: "<workflow-path> run_id=<run-id> [key=value ...] [stop_after_step=<step>]"
license: MIT
---

# Run Engineering Workflow — 4.0

## Mission

Turn skills + prompt packs into a controlled multi-stage agentic workflow.

Do not improvise the lifecycle when a workflow file exists.

## Runtime Methodology-Immutability Rule

For normal engineering/reverse-engineering workflow execution, the methodology infrastructure is read-only:

```text
.ai-engineering/
.github/
```

A workflow run MUST NOT create, modify, rename, or delete prompts, workflows, skills, agent definitions, or Copilot instructions under those directories. Runtime analysis artifacts and workflow state must be written only to workflow-declared output/state paths.

If a referenced prompt/workflow/skill is missing or incompatible, STOP and report the missing/incompatible asset. Do not synthesize a replacement helper prompt/workflow/skill during the run.

The only exception is an explicit package-maintenance task whose user request is to modify the methodology package itself.

## Mental Model

```text
workflow = control plane
prompt   = concrete task contract
skill    = reusable methodology
repo     = evidence source
artifact = persistent result
gate     = transition decision
```

## Inputs

Required:

- workflow file
- workflow input values
- current repository

Optional:

- existing workflow state for resume

If a correctness-critical required workflow input is missing, return:

`WORKFLOW_INPUT_REQUIRED`

Do not invent it.

For every required input whose value is an artifact/file path, verify the file exists before executing
the first substantive stage. A path mentioned by a generated document is not evidence of existence.

- missing required artifact => `REQUIRED_INPUT_ARTIFACT_MISSING` and STOP
- incompatible/mismatched declared upstream provenance => `UPSTREAM_PROVENANCE_MISMATCH` and STOP

Do not reconstruct a missing upstream artifact inside a downstream workflow.

## Workflow Resolution

Load the named workflow from:

```text
.ai-engineering/workflows/
```

or the exact path supplied by the user.

Resolve `{{variable}}` placeholders only from:

1. explicit user input
2. workflow defaults
3. already persisted workflow state
4. runner-owned immutable values explicitly defined by this contract

The runner MUST load `.ai-engineering/package-version.yaml` and expose its `package_version` as
`agent_package_version`. A workflow MUST NOT duplicate or override that value.

Do not infer requirement paths, patch paths, scopes, or output roots when multiple choices exist.

## Stage Execution

### Delegation Contract

The runner resolves `execution.delegation_mode` with this rule:

```text
missing        -> direct_only
direct_only    -> execute in current custom-agent session
bounded        -> delegated attempt allowed with mandatory direct fallback
```

For `direct_only`:

1. MUST NOT invoke a General-purpose agent, background agent, or asynchronous worker to own the stage;
2. MUST use repository/tool operations directly from the current agent session;
3. MUST NOT wait for or poll another agent;
4. MUST write and validate the workflow-declared artifact before transition.

For `bounded` delegation:

1. the current stage remains owned by the parent workflow runner;
2. the delegated task must have the same bounded stage scope and declared output;
3. delegated completion is accepted only when the declared stage artifact exists and has a valid gate;
4. on the first `idle`, no-progress, missing-output, or unavailable-worker observation, stop polling;
5. immediately continue the same stage by direct execution in the parent agent;
6. never count worker status (`running`, `idle`, `completed`) as a workflow gate.

This policy prevents orchestration deadlocks such as:

```text
delegate stage -> wait -> idle -> poll -> idle -> poll ...
```

The workflow state machine advances only from validated artifacts, never from sub-agent status.

For the current stage:

1. persist `ACTIVE_STEP`
2. load only the stage's declared inputs/artifacts plus targeted current source
3. read the referenced prompt
4. apply the named skill(s)
5. obey the prompt's source-of-truth and output rules
6. write the declared artifact
7. read the artifact's final structured `WORKFLOW_GATE`
8. validate that the status is allowed for this stage
9. persist the gate result
10. follow the workflow transition

Do not collapse multiple substantive stages into one reasoning pass.

A stage boundary is a **checkpoint**, not a task-completion boundary.

After a stage artifact and gate are validated and the workflow transition resolves to another
non-terminal step, immediately continue that next step as the next reasoning continuation in
the **same Autopilot task**. Do not return `task_complete`, "Task complete", or an equivalent
final answer merely because an intermediate stage completed.

Only a terminal workflow state (`DONE`, `BLOCKED`, an unavoidable input-required condition,
or an explicit `stop_after_step`) ends the user task.




## Invocation Binding Rules

Treat workflow selection and input binding deterministically from the user's invocation text.

### Workflow selection

If the user prompt contains exactly one explicit workflow path matching:

```text
.ai-engineering/workflows/*.yaml
```

that path is the selected workflow.

In that case:

- do not enumerate available workflows;
- do not ask which workflow to run;
- do not replace the explicit path with another candidate;
- load that exact workflow definition.

If the user supplies a workflow filename without the directory and it uniquely matches one file
under `.ai-engineering/workflows/`, bind that unique file directly.

Ask the user to select a workflow only when:

- no workflow path/name is present; or
- multiple explicit workflow candidates are supplied and intent is genuinely ambiguous.

### Input binding

Bind explicit `key=value` tokens from the invocation directly to workflow inputs.

Example:

```text
/run-engineering-workflow .ai-engineering/workflows/full-reverse-engineering.yaml run_id=20260904
```

binds:

```yaml
workflow: .ai-engineering/workflows/full-reverse-engineering.yaml
inputs:
  run_id: "20260904"
```

Do not ask again for `run_id` or any other required input already explicitly supplied.

For multiline invocations such as:

```text
/run-engineering-workflow

Run:
.ai-engineering/workflows/full-reverse-engineering.yaml

Inputs:
run_id=20260904
```

treat the `Run:` path and `Inputs:` assignments exactly the same way.

Ask for clarification only for required inputs that are genuinely absent or ambiguous.

### No redundant discovery

Once an explicit workflow has been bound, do not list the workflow directory merely to ask the
user which workflow to choose. Directory inspection is allowed only when needed to validate
that the supplied workflow path exists or to resolve an unqualified unique workflow name.

## Autopilot Continuation Contract

For a workflow invocation in GitHub Copilot CLI Autopilot mode, distinguish:

```text
reasoning continuation
    = one bounded stage execution/checkpoint

user task
    = the entire requested workflow run
```

Canonical behavior:

```text
execute active stage
→ write declared artifact
→ validate WORKFLOW_GATE
→ persist workflow transition
→ terminal state?
   YES → finish the user task
   NO  → immediately continue the next stage in the same Autopilot task
```

Intermediate stage statuses are workflow transition gates, not task-completion signals.

The runner MUST NOT announce `Task complete`, emit a final workflow summary, or otherwise
signal task completion while the persisted workflow state has a non-terminal `active_step`.

A concise progress update between continuations is allowed, but execution must continue
automatically.

Terminal task completion is legal only when:

1. the workflow transition resolves to `DONE`;
2. the workflow transition resolves to `BLOCKED`;
3. a required input is missing and continuation is impossible;
4. an explicit `stop_after_step` has been reached; or
5. the Copilot CLI Autopilot continuation ceiling is reached.

If the CLI continuation ceiling is reached before a workflow terminal state, persist exact
resume state and report `PARTIAL_RESUMABLE`; do not mark the workflow complete.


## Inclusive Stop-After-Step Control

The runner supports an optional execution control:

```yaml
stop_after_step: <workflow-step-id | null>
```

Semantics are **inclusive**:

```text
execute stop_after_step
→ validate and persist its artifact + gate
→ compute/persist the workflow-derived next step
→ STOP before executing that next step
```

If `stop_after_step` is not a declared workflow step, return `WORKFLOW_INPUT_REQUIRED` and STOP.
Do not interpret free-text phrases such as "through X" or "stop before Y" when an explicit `stop_after_step` control is available.

When stopping intentionally after the requested step, return `PARTIAL_RESUMABLE`; this is not a failed gate. The persisted state must identify the next executable workflow step.

## Declared Output Enforcement

For every stage with a workflow-declared `output`:

1. write exactly that output path;
2. verify the file exists before reading its gate;
3. reject a same-purpose file at a legacy/shared path as stale;
4. do not substitute an undeclared summary artifact for the stage output.

Missing declared stage output => `STAGE_OUTPUT_MISSING` and STOP.

A stage whose workflow transition points to an independent verifier is not complete for downstream progression until that verifier's declared output exists and its gate passes.

## Structured Gate Rule

Every workflow-managed stage must end its artifact with exactly one block:

```yaml
WORKFLOW_GATE:
  workflow: <workflow-name>
  step: <step-id>
  status: <allowed-status>
  unresolved_critical: <integer>
  unresolved_high: <integer>
  source_resolvable_open: <integer>
  artifact: <path>
  next_recommended: <step-id-or-null>
```

If the block is missing or malformed:

`GATE_RESULT_MISSING`

Do not infer PASS from prose.

## High-Impact Unknown Rule

When a transition routes to unknown resolution:

- before entering the resolver, persist `blocking_artifact` as the gate artifact that triggered resolution
- persist `blocking_qids` as the exact unresolved HIGH/CRITICAL Q-IDs from that gate/state
- persist `blocking_retry_step` as the exact workflow step to retry
- require the resolver step to bind all three values explicitly through its `inputs`
- run `/resolve-high-impact-unknowns`
- resolve only those blocking Q-IDs
- persist evidence/closure state
- return only to `blocking_retry_step`

Do not silently continue to design/test while source-resolvable HIGH/CRITICAL gaps remain.

## Evidence Rules

- current source remains stronger than generated artifacts
- prior artifacts are inputs, not unquestionable truth
- reverify high-impact findings against source when a later step depends on them
- requirements define intended behavior, not current implementation
- patches/designs are candidate future behavior
- unresolved mappings remain UNKNOWN

## Workflow State

Persist active workflow state to the workflow-declared `state_path`.

For run-scoped workflows this is normally:

```text
docs/reverse-engineering/runs/<run_id>/workflow_state.yaml
```

A `.yaml` workflow state file MUST contain valid YAML, not Markdown/prose.

Minimum fields:

```yaml
workflow:
run_id:
status:
inputs:
active_step:
completed_steps:
failed_or_blocked_steps:
last_gate:
unresolved_qids:
blocking_artifact:
blocking_qids:
blocking_retry_step:
artifacts:
resume_instruction:
```

For a run-scoped workflow, `state_path` is the single authoritative run state.

MUST NOT create or update either of these inside `docs/reverse-engineering/runs/<run_id>/`:

```text
00_workflow_state.md
workflow_state.md
```

The full-reverse-engineering workspace also uses its workflow-declared YAML state file.
No Markdown workflow-state mirror is authoritative or required.

## Stop Conditions

Use:

- `WORKFLOW_COMPLETE`
- `WORKFLOW_BLOCKED_SOURCE_GAPS`
- `WORKFLOW_BLOCKED_EXTERNAL_EVIDENCE`
- `WORKFLOW_INPUT_REQUIRED`
- `PARTIAL_RESUMABLE`
- `GATE_RESULT_MISSING`

Never call the workflow complete because the narrative "looks good".

## Console Discipline

Console output should normally contain only:

- workflow status
- active/completed step
- blocking Q-IDs
- latest artifact
- exact next action


## Nested Workflow / Phase Support

A workflow may contain `phases` that reference other workflow files.

For each phase:

1. resolve explicit/derived inputs
2. run the child workflow to its terminal gate
3. persist child run ID and artifacts
4. continue only when the child terminal status matches the parent's allowed status

Do not flatten multiple child workflows into one mega-prompt.

## Child Workflow Step Support

A normal `steps` state machine may invoke a child workflow using:

```yaml
child_workflow: .ai-engineering/workflows/<child>.yaml
inputs: {...}
execution:
  execution_mode: fresh | resume
  ignore_previous_completion: true | false
statuses: {...}
```

For a child workflow step, the runner MUST:

1. resolve every child input explicitly;
2. validate the child workflow file exists;
3. validate all child required inputs before execution;
4. honor the child execution controls, including fresh execution;
5. execute the child with its own declared state path;
6. persist the child terminal status and artifacts in the parent state;
7. route only through the parent step's declared `statuses`.

Do not flatten the child into the parent's reasoning context. A child marked `fresh` must re-read its
workflow, prompts, skills, source artifacts, and source repository from disk and must not inherit a prior
verdict as proof.

## `foreach` Artifact Loop Support

A workflow may define a `foreach` stage over a registry artifact.

The runner must:

1. parse only structured registry rows/items explicitly identified by the workflow
2. order items by declared dependency ordering when available
3. persist the active item ID
4. execute one item's design/verification cycle at a time
5. update registry status after each verified item
6. revisit deferred items after dependencies are verified
7. stop on unresolved dependency cycles rather than inventing an order

For design-artifact loops:

```text
one Artifact ID
→ detailed design
→ independent verification
→ VERIFIED?
   YES → next artifact
   NO  → revise/resolve/reverify same artifact
```

Do not generate detailed design for all artifacts in one reasoning pass merely to save time.
If `foreach.bindings` is declared, resolve per-item variables only from those bindings. Supported binding forms are:

```yaml
bindings:
  artifact_id:
    field: Artifact ID
  artifact_name:
    field: Name
  artifact_slug:
    field: Name
    transform: slugify
```

`slugify` is deterministic: lowercase, replace non-alphanumeric runs with `-`, trim leading/trailing `-`.
Do not infer alternate registry columns when a declared field is missing; stop with `WORKFLOW_INPUT_REQUIRED`.


## Registry Gate Rule

When workflow progression depends on a registry (for example, design artifacts),
the runner must verify the registry state rather than relying on prose summaries.

If the workflow requires all required artifacts to be VERIFIED:

- every applicable registry row must show VERIFIED
- missing rows/statuses are blockers
- do not infer completion from the number of generated files

## Design/WBS Revision Loops

Verification stages must not silently edit the artifact they are verifying.

Use:

```text
generate
→ verify independently
→ findings
→ explicit revision step
→ reverify
```

This preserves an audit trail and reduces self-confirming reasoning.


# 4.0 Execution Semantics

Supported execution controls:

```yaml
execution_mode: resume | fresh
ignore_previous_completion: true | false
```

Defaults when omitted:

```yaml
execution_mode: resume
ignore_previous_completion: false
```

## Resume

`execution_mode: resume` reuses persisted state and continues from the next incomplete step.

## Fresh

`execution_mode: fresh` means:

- re-read the current workflow YAML from disk
- re-read every referenced prompt and skill from disk
- execute the workflow again from its first applicable step
- do not satisfy the request by summarizing a previous execution
- previous final verdicts are historical evidence only
- prior artifacts may be inputs only when the workflow explicitly references them

## Ignore Previous Completion

When:

```yaml
ignore_previous_completion: true
```

a prior `DONE`, `COMPLETE`, `IMPLEMENTATION_READY`, `POST_READINESS_AUDIT_PASS*`, or other terminal
state MUST NOT cause execution to be skipped.

The assistant MUST NOT respond only with "already completed" or a previous summary.

If `ignore_previous_completion: true` is supplied without `execution_mode`, treat it as:

```yaml
execution_mode: fresh
```

Canonical rule:

```text
if execution_mode == fresh
OR ignore_previous_completion == true:
    previous completion != current execution
```

If a fresh execution cannot actually run because required files/inputs are unavailable, return:

`WORKFLOW_FRESH_EXECUTION_BLOCKED`

with the missing input. Do not reuse the old verdict.

When supported by the state format, record:

```yaml
execution_mode: fresh
ignore_previous_completion: true
fresh_execution_of: <prior-run-id-or-null>
```


# 4.0 Workflow Contract Safety

Before executing a workflow after package changes, the runner should verify that its task contracts
are internally routable.

Canonical invariant:

```text
EMITTED_GATE_STATUS ⊆ WORKFLOW_ALLOWED_STATUS
```

For prompts with an explicit final `WORKFLOW_GATE` status union:

```text
PROMPT_DECLARED_STATUS = WORKFLOW_ALLOWED_STATUS
```

If a task/skill emits a status that the active workflow does not route:

`WORKFLOW_STATUS_CONTRACT_VIOLATION`

Do not ignore the status, coerce it to PASS, or continue to the next stage.

Package validator:

```bash
python .ai-engineering/tools/validate-workflow-contracts.py
```

A failing validator blocks workflow execution until the contract is corrected.


# 4.0 Run Isolation and Provenance

## Fresh Run Isolation

For `execution_mode: fresh`:

1. `run_id` is REQUIRED.
2. Resolve `artifact_root` to `docs/reverse-engineering/runs/<run_id>` unless the user explicitly supplies an equivalent run-scoped path. A workflow default/shared root MUST NOT override this rule.
3. The workflow `state_path` and every generated stage output for the fresh run must resolve under that same run root.
4. Create/read only workflow outputs under that run root.
4. Legacy/shared generated artifacts outside the run root are STALE by default.
5. A stale artifact MUST NOT satisfy a current-run precondition or gate.
6. If a stage output expected for the current run does not exist, the stage is NOT complete even if a same-named legacy file exists elsewhere.

Canonical rule:

```text
artifact.run_id == active run_id
AND artifact.agent_package_version == active package version
AND artifact.source_commit == active source commit (when source commit is applicable)
```

Otherwise:

`STALE_ARTIFACT_REJECTED`

## Run Manifest

At run-scoped workflow initialization, create the manifest for a fresh run or for a first-time resume when no run state exists:

`docs/reverse-engineering/runs/<run_id>/RUN_MANIFEST.yaml`

Minimum fields:

```yaml
agent_package_version:
run_id:
workflow:
execution_mode:
source_commit:
started_at:
last_updated:
status:
artifacts:
```

For each completed stage persist exact artifact path + gate status + provenance.

Downstream stages MUST resolve generated inputs from this manifest/state. Never reconstruct a path from
scope alone when the manifest contains the exact path.

## Latest Pointer

Maintain `docs/reverse-engineering/LATEST_RUN.md` as a convenience pointer only.
It must contain the current run ID and run manifest path.

Never use it as evidence in place of the manifest/state.

## No Universal Shared Output in Fresh Mode

Fresh runs MUST NOT overwrite or consume:

```text
docs/reverse-engineering/design/00_design_artifact_registry.md
docs/reverse-engineering/implementation/<scope>_wbs.md
docs/reverse-engineering/implementation/<scope>_wbs_verification.md
docs/reverse-engineering/implementation/<scope>_implementation_readiness.md
docs/reverse-engineering/audits/<scope>_post_readiness_audit.md
```

Those are legacy compatibility paths only.


# 4.0 Stable Filename Rule

Run identity is carried by the run directory and manifest, not the filename.

Generated artifact filenames MUST NOT append:

- package version
- date
- timestamp
- run ID

Use stable names inside `docs/reverse-engineering/runs/<run_id>/`.

Examples:

```text
workflow_state.yaml
verification/tdd_verification.md
design/design_artifact_registry.md
implementation/wbs.md
implementation/wbs_verification.md
implementation/implementation_readiness.md
audits/post_readiness_audit.md
```

If history is required, create another run directory or attempt directory. Do not mutate filenames
to encode history.


# 4.0 Normative Methodology Checkpoint

Before executing or changing workflow behavior, read:

`docs/METHODOLOGY_BASELINE.md`

It is normative. Workflow mechanics must preserve its purpose, boundary, and quality targets.

Do not reinterpret a bug fix as permission to expand the agent into implementation, effort estimation,
or a general autonomous SDLC system.

# 4.0 Transactional Workflow-State Integrity

The workflow definition is authoritative for transitions.

`WORKFLOW_GATE.next_recommended` is advisory only and MUST NOT override the workflow transition map.

For every completed stage/item, perform one atomic logical update:

```text
1. validate emitted gate
2. determine workflow transition from workflow YAML
3. mark current stage/item completed or blocked
4. compute next executable stage/item
5. set active_step/current_item to that next executable unit
6. persist exact artifact path
7. persist workflow_state.yaml once
```

Required invariants:

```text
completed item != next executable item
active_step == workflow-derived next executable step
next_action == workflow-derived next executable action
artifact path == workflow-declared output path
workflow_state.yaml parses as YAML
```

If any invariant fails:

`WORKFLOW_STATE_INTEGRITY_VIOLATION`

Stop instead of resuming from contradictory state.

Do not store duplicated free-text "Next Action" sections inside `workflow_state.yaml`.
Human-readable summaries may be written separately as `.md`, but machine state must remain structured
YAML.


## Package maintenance rule
Before changing/releasing the agent package, re-read `docs/PACKAGE_MAINTENANCE_RULES.md` and `docs/METHODOLOGY_BASELINE.md` from the exact predecessor package.