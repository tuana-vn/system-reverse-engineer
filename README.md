# System Reverse Engineer

Evidence-backed reverse engineering agent and reusable skills for GitHub Copilot.

The package is designed for unfamiliar, legacy, and large codebases where a plausible explanation is not enough. It separates **discovery** from **certification**, keeps a repository-backed evidence ledger, actively searches for counterexamples, and refuses to declare a baseline ready while source-resolvable high-impact gaps remain.

## What problem does it solve?

Large-codebase reverse engineering often fails in one of two ways:

1. the agent explores quickly but turns plausible guesses into architecture facts; or
2. the agent becomes so conservative that it produces shallow analysis full of `UNKNOWN` without exhausting the source.

V3.0 uses a two-mode model:

```text
DISCOVERY MODE
  aggressively explore source and reconstruct candidate architecture

CERTIFICATION MODE
  verify, falsify, scope, and promote only defensible claims
```

The default lifecycle is:

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

## Repository layout

```text
.github/
  agents/
    system-reverse-engineer.agent.md
  skills/
    .../SKILL.md
  copilot-instructions.md

docs/
  RUNBOOK.md
  MIGRATION_V2.1_TO_V3.0.md

CHANGELOG.md
LICENSE
README.md
```

The repository uses GitHub's supported project-level locations for custom agents and agent skills:

- custom agent: `.github/agents/`
- agent skills: `.github/skills/<skill-name>/SKILL.md`
- repository instructions: `.github/copilot-instructions.md`

## Included skills

### Core reverse engineering

| Skill | Purpose |
|---|---|
| `reverse-engineering-bootstrap` | Initialize repository-backed memory, workflow state, baseline identity, and broad reconnaissance. |
| `full-reverse-engineering` | Orchestrate the end-to-end V3.0 workflow. |
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

V3.0 public release intentionally excludes incident-RCA and observability-specific helper skills. They are useful disciplines, but they are not required for the core reverse-engineering lifecycle and made the package less focused.

## Install into a project repository

From the root of the repository you want to analyze:

```bash
mkdir -p .github/agents .github/skills
cp /path/to/system-reverse-engineer/.github/agents/system-reverse-engineer.agent.md .github/agents/
cp -R /path/to/system-reverse-engineer/.github/skills/* .github/skills/
```

Review `.github/copilot-instructions.md` before copying it into an existing project because your project may already have repository-wide Copilot instructions. If it does not:

```bash
cp /path/to/system-reverse-engineer/.github/copilot-instructions.md .github/copilot-instructions.md
```

If the target already has `.github/copilot-instructions.md`, merge the reverse-engineering rules instead of overwriting project-specific instructions.

## Install for personal Copilot CLI use

GitHub Copilot CLI supports user-level custom agents in `~/.copilot/agents` and user-level skills in `~/.copilot/skills`.

```bash
mkdir -p ~/.copilot/agents ~/.copilot/skills
cp .github/agents/system-reverse-engineer.agent.md ~/.copilot/agents/
cp -R .github/skills/* ~/.copilot/skills/
```

For project-specific behavior, repository-level installation is preferred because the reverse-engineering baseline is stored alongside the analyzed repository.

## Quick start

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
  00_workflow_state.md
  00_investigation_coverage.md
```

For a later session:

```text
Use /resume-reverse-engineering.
```

For detailed operating procedures, readiness rules, and common workflows, see [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Readiness states

V3.0 uses explicit readiness states:

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
