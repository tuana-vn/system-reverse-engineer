# System Reverse Engineer 4.0

> Normative purpose/boundary/quality contract: `docs/METHODOLOGY_BASELINE.md`

Evidence-backed reverse engineering agent and reusable skills for GitHub Copilot.

The package is designed for unfamiliar, legacy, and large codebases where a plausible explanation is not enough. It separates **discovery** from **certification**, keeps a repository-backed evidence ledger, actively searches for counterexamples, and refuses to declare a baseline ready while source-resolvable high-impact gaps remain.

## What problem does it solve?

Large-codebase reverse engineering often fails in one of two ways:

1. the agent explores quickly but turns plausible guesses into architecture facts; or
2. the agent becomes so conservative that it produces shallow analysis full of `UNKNOWN` without exhausting the source.


```text
DISCOVERY MODE
  aggressively explore source and reconstruct candidate architecture

CERTIFICATION MODE
  verify, falsify, scope, and promote only defensible claims
```

The evidence lifecycle remains:

```text
aggressive discovery
→ evidence hardening
→ high-impact unknown closure
→ adversarial coverage/readiness audit
→ canonical baseline
```

## Key ideas

- **Current source beats generated memory.** Generated Markdown is an accelerator, never a stronger source of truth than the code and runtime evidence that produced it.
- **Candidate claims are not canonical facts.** Claims move through explicit verification and promotion gates.
- **Counterexample search is mandatory.** Alternate implementations, configuration branches, fallbacks, test-only wiring, legacy paths, and model/version switches are searched before broad claims are promoted.
- **High-impact unknowns must be closed.** A source-resolvable HIGH/CRITICAL gap blocks readiness.
- **Coverage is audited.** The workflow looks for architecture domains that were never investigated, not only contradictions in what was already documented.
- **The repository is persistent memory.** Copilot conversations are disposable working context.

## Recommended GitHub Copilot CLI execution

For full multi-stage reverse engineering, start the CLI in **Autopilot** mode:

```bash
copilot --mode autopilot --max-autopilot-continues 20
```

Then use `/agent` and select:

```text
system-reverse-engineer
```

Invoke:

```text
/run-engineering-workflow .ai-engineering/workflows/full-reverse-engineering.yaml run_id=YYYYMMDD
```

The requested task is the **whole workflow**, not one stage. The canonical full-baseline deliverable is `docs/reverse-engineering/CURRENT_STATE_TDD.md` plus five evidence-linked Mermaid architecture/runtime diagrams. Each stage is executed and
checkpointed separately, then Autopilot continues to the workflow-derived next stage until a
terminal state is reached.

`--max-autopilot-continues` is a CLI safety ceiling. If the ceiling is reached before the
workflow reaches a terminal state, resume the same `run_id`. Omitting the option uses the
CLI's default continuation limit.


## controlled engineering-agent model

4.0 provides first-class **prompts + declarative workflows** above reusable skills:

```text
agent
→ workflow/state machine
→ task prompt
→ skill(s)
→ current repository/evidence
→ artifact
→ structured gate
→ next state
```

This prevents the agent from assuming that a generic skill alone contains enough
feature-specific scope to safely perform high-impact analysis/design.

The workflow YAML is a repository convention interpreted by the agent; it is not a
deterministic GitHub-native workflow runtime.

See:
- `docs/METHODOLOGY.md`
- `docs/CONTEXT_FOR_FUTURE_SESSIONS.md`
- `.ai-engineering/workflows/`
- `.ai-engineering/prompts/`


## Use-case-first operation


4.0 adds an operational navigation layer:

```text
engineering problem
→ use case
→ workflow
→ prompts + skills
→ artifacts + gates
```

Start here:

- `docs/USE_CASE_CATALOG.md` — which workflow fits the problem?
- `docs/WORKFLOW_MATRIX.md` — workflow inputs/outputs/success gates
- `docs/SKILL_MATRIX.md` — what each installed skill is for
- `docs/USE_CASE_SKILL_WORKFLOW_MATRIX.md` — end-to-end mapping
- `docs/RUNBOOK.md` — copyable execution commands

New use-case workflows include:
- targeted source analysis
- architecture drift/rebaseline
- incident RCA
- observability/traceability analysis


## Repository layout

```text
.github/agents/
  system-reverse-engineer.agent.md

.github/skills/
  .../SKILL.md
  run-engineering-workflow/SKILL.md

.ai-engineering/workflows/
  full-reverse-engineering.yaml
  targeted-source-analysis.yaml
  patch-impact-to-tests.yaml
  requirement-to-design.yaml
  design-to-implementation.yaml
  requirement-to-implementation-plan.yaml
  claim-justification.yaml
  architecture-drift-rebaseline.yaml
  incident-root-cause-analysis.yaml
  observability-traceability-analysis.yaml

.ai-engineering/prompts/
  requirement-to-design/
  patch-impact-to-tests/
  claim-justification/
  common/

.ai-engineering/schemas/
.ai-engineering/state-templates/

docs/
  RUNBOOK.md
  USE_CASE_CATALOG.md
  WORKFLOW_MATRIX.md
  SKILL_MATRIX.md
  USE_CASE_SKILL_WORKFLOW_MATRIX.md
  METHODOLOGY.md
  CONTEXT_FOR_FUTURE_SESSIONS.md

.github/copilot-instructions.md
LICENSE
README.md
```

The package keeps its Copilot runtime assets together under:

- custom agent: `.github/agents/`
- agent skills: `.github/skills/<skill-name>/SKILL.md`
- package instructions: `.github/copilot-instructions.md`

## Included skills

### Core reverse engineering

| Skill | Purpose |
|---|---|
| `reverse-engineering-bootstrap` | Initialize repository-backed memory, workflow state, baseline identity, and broad reconnaissance. |
| `full-reverse-engineering` | Orchestrate the end-to-end 4.0 workflow. |
| `resume-reverse-engineering` | Rehydrate a fresh Copilot session without restarting the analysis. |
| `runtime-flow-analysis` | Trace an operation end-to-end from trigger to concrete boundary and result mapping. |
| `integration-selection-analysis` | Reconstruct routing and selection rules without over-generalizing them. |
| `configuration-source-trace` | Trace behavior-changing configuration from source/defaults to runtime consumers. |
| `runtime-binding-verification` | Prove which concrete implementation is actually active and under what conditions. |
| `persistence-schema-reverse-engineering` | Reconstruct persistence wiring and code-supported schema knowledge. |
| `claim-verification-and-promotion` | Verify candidate claims and promote only evidence-backed statements. |
| `resolve-high-impact-unknowns` | Actively close HIGH/CRITICAL unknowns before readiness. |
| `reverse-engineering-coverage-audit` | Find important architectural areas that were never investigated deeply enough. |
| `adversarial-baseline-audit` | Try to disprove promoted claims and expose stale or over-broad conclusions. |
| `architecture-drift-detection` | Compare the stored baseline with current source after the codebase changes. |
| `baseline-source-of-truth-maintenance` | Safely rebaseline verified current behavior while preserving evidence history. |

### Baseline-powered engineering workflows

| Skill | Purpose |
|---|---|
| `patch-impact-review` | Review a diff against the verified current-system baseline. |
| `requirement-compliance-review` | Compare atomic requirements with implemented patch behavior. |
| `regression-test-design` | Derive focused regression coverage from rules, flows, changes, and risks. |
| `technical-design-proposal` | Produce a source-backed technical design before implementation. |
| `contract-impact-test-design` | Derive contract-level test viewpoints and matrices from verified impact/design. |
| `run-engineering-workflow` | Execute prompt/skill workflows with structured gates and persistent state. |

The current package also contains incident-RCA and observability/traceability helper skills.
They are optional supporting disciplines and are not required by every core workflow.

## Install into a project repository

Overlay the package directories at the target repository root so `.ai-engineering/`, `.github/`, and `docs/` remain repository-relative exactly as referenced by workflows and skills.

Do not move package-internal assets to alternate paths unless you also intentionally adapt every affected reference.

## Install for personal Copilot CLI use

GitHub Copilot CLI supports user-level custom agents in `~/.github/agents` and user-level skills in `~/.github/skills`.

```bash
mkdir -p ~/.github/agents ~/.github/skills
cp .github/agents/system-reverse-engineer.agent.md ~/.github/agents/
cp -R .github/skills/* ~/.github/skills/
```

For project-specific behavior, repository-level installation is preferred because the reverse-engineering baseline is stored alongside the analyzed repository.


## requirement-to-design execution integrity

4.0 makes the independent requirement-gap verifier an executable, auditable stage rather than an advisory concept. Fresh requirement-to-design artifacts are run-scoped, `stop_after_step` is explicit and inclusive, Stage 02 cannot claim direct readiness for technical design before Stage 02B, and source questions required by authoritative TDD questions must be resolved before TDD instead of deferred into design.

## Maintenance and tooling

4.0 consolidates the runtime validation surface. Version-specific regression validators are not delivered as permanent runtime commands. Semantic correctness is checked by independent workflow verifiers; Python remains limited to generic deterministic mechanical checks. Normal installation is a repository overlay, not a dedicated package-only repo. See `docs/PACKAGE_MAINTENANCE_RULES.md`.

## Quick start

For requirement-to-design work:

```text
Use the one-line workflow skill invocation. Example:

```text
/run-engineering-workflow .ai-engineering/workflows/requirement-to-design.yaml requirement_path=<path> scope=<scope> scope_slug=<slug>
```

Required inputs are:
requirement_path=<path>
scope=<scope>
scope_slug=<safe-name>
```

The agent will run analysis → gap analysis → unknown resolution when needed → TDD → test design,
one gated stage at a time.


Select the custom agent in Copilot, then start with:

```text
Use /full-reverse-engineering.
```

The workflow creates and maintains:

```text
docs/reverse-engineering/
  00_current_understanding.md
  00_evidence_ledger.md
  00_master_decision_matrix.md
  00_hypotheses.md
  00_open_questions.md
  workflow_state.yaml
  00_investigation_coverage.md
```

For a later session:

```text
Use /resume-reverse-engineering.
```

For detailed operating procedures, readiness rules, and common workflows, see [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Readiness states

4.0 uses explicit readiness states:

```text
BASELINE_READY
BASELINE_READY_WITH_EXTERNAL_BLOCKERS
NOT_READY_HIGH_IMPACT_GAPS
PARTIAL_RESUMABLE
```

`BASELINE_READY` requires zero unresolved source-resolvable HIGH/CRITICAL gaps and no HIGH/CRITICAL coverage gap.

## Safety and evidence rules

This project does not make proprietary code safe to share with an AI service. You are responsible for the confidentiality, licensing, security, and data-handling rules of the repository being analyzed.

Recommended practice:

- use the package only in environments where the selected Copilot deployment is authorized for the source code;
- never copy secrets or sensitive artifacts into prompts unless the environment explicitly permits it;
- treat tests as supporting evidence, not proof of active production wiring;
- do not promote unmerged patches, requirements, proposals, or incident hypotheses into the current-system baseline;
- preserve evidence history when a claim is corrected or superseded.

## Compatibility

The layout follows current GitHub Copilot project conventions for custom agents and agent skills. GitHub may evolve these features over time; consult the official GitHub Copilot customization documentation if a future version changes discovery locations or frontmatter fields.

## License

MIT. See [LICENSE](LICENSE).

## Contributing

Issues and pull requests are welcome. Useful contributions include:

- tighter evidence/promotion gates;
- better counterexample-search strategies;
- language/framework-specific source-tracing patterns that remain generic;
- reproducible examples using synthetic or open-source systems;
- reduced prompt/context cost without weakening verification.

Please do not contribute proprietary code, confidential architecture, credentials, internal hostnames, customer identifiers, or examples copied from restricted projects.


## Design-to-implementation pipeline

The current planning pipeline is:

```text
verified inputs
-> TDD verification
-> design artifact decomposition
-> independent decomposition verification
-> per-artifact detailed design
-> independent per-artifact verification
-> WBS generation
-> independent WBS verification
-> implementation-readiness certification
-> fresh post-readiness child workflow
```

The pipeline uses run-scoped artifacts, explicit provenance, deterministic foreach bindings, and one authoritative YAML state file per workflow.

## Package validation

Run the generic validators before using or delivering the package:

```bash
python .ai-engineering/tools/validate-package-layout.py
python .ai-engineering/tools/validate-methodology-baseline.py
python .ai-engineering/tools/validate-workflow-contracts.py
```

For an extracted delivery package, also run `validate-package-layout.py --strict-package-root`.
