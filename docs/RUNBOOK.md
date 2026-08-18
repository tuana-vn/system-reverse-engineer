# System Reverse Engineer V3.0 — Runbook

This runbook is the shortest operational path for using the package on a real repository.

## 1. Preconditions

Before starting:

- the repository is checked out at the branch/commit you intend to analyze;
- Copilot is allowed to access that source code under your organization/project policy;
- the System Reverse Engineer agent and skills are installed;
- generated reverse-engineering artifacts will be written under `docs/reverse-engineering/`;
- you know whether this is a new baseline, a continuation, or a review of an existing baseline.

Do not begin by pasting an architecture story into the prompt. Let source discovery build the candidate model.

## 2. New repository: full baseline

Select the `system-reverse-engineer` custom agent and run:

```text
Use /full-reverse-engineering.
```

Expected high-level lifecycle:

```text
bootstrap
→ broad discovery
→ runtime/config/binding/persistence tracing
→ claim verification and promotion
→ HIGH/CRITICAL unknown closure
→ adversarial baseline audit
→ coverage audit
→ readiness certification
```

Do not accept `BASELINE_READY` if source-resolvable HIGH/CRITICAL gaps remain.

## 3. Fresh chat/session: resume

Use:

```text
Use /resume-reverse-engineering.
```

The resume workflow should reconstruct working context from repository artifacts, especially:

```text
00_workflow_state.md
00_current_understanding.md
00_master_decision_matrix.md
00_open_questions.md
00_investigation_coverage.md
```

Do not restart full reverse engineering merely because the conversation context was lost.

## 4. Close important unknowns

Use:

```text
Use /resolve-high-impact-unknowns.
```

A HIGH/CRITICAL question should not be marked externally blocked until repository search coverage is recorded and the exact missing external evidence is named.

Allowed closure states:

```text
SOURCE_SEARCH_PENDING
SOURCE_SEARCH_IN_PROGRESS
SOURCE_EXHAUSTED
EXTERNALLY_BLOCKED
RESOLVED_VERIFIED
RESOLVED_REJECTED
NOT_APPLICABLE
```

## 5. Trace one operation deeply

Use:

```text
Use /runtime-flow-analysis for <operation>.
```

Expected trace shape:

```text
inbound trigger
→ entry handler
→ validation/conversion
→ service/use case
→ orchestration
→ abstraction
→ selector/factory/provider
→ concrete implementation
→ external/persistence boundary
→ response/error mapping
```

Important findings start as candidates. Promote them only after source verification, counterexample search, and scope checks.

## 6. Prove routing or implementation selection

For a routing matrix or backend/client selection rule:

```text
Use /integration-selection-analysis for <selection scope>.
```

For the concrete runtime implementation behind an abstraction:

```text
Use /runtime-binding-verification for <abstraction or client>.
```

Use both when a high-impact claim depends on both a business selection rule and actual DI/factory/bootstrap wiring.

## 7. Trace behavior-changing configuration

Use:

```text
Use /configuration-source-trace for <configuration key or behavior>.
```

Trace:

```text
external/default definition
→ loader
→ override/precedence
→ runtime representation
→ consumer branch
→ selected behavior
```

Do not infer runtime behavior from a configuration key name alone.

## 8. Reverse engineer persistence

If persistence exists:

```text
Use /persistence-schema-reverse-engineering for <domain/repository>.
```

Separate:

- schema facts proven by source/migrations/DDL;
- ORM/repository behavior proven by code;
- runtime/database state that is external to the repository.

## 9. Audit before declaring the baseline ready

Run:

```text
Use /adversarial-baseline-audit.
Use /reverse-engineering-coverage-audit.
```

The adversarial audit attacks promoted claims.
The coverage audit searches for important source areas that never became claims at all.

Readiness:

```text
BASELINE_READY
BASELINE_READY_WITH_EXTERNAL_BLOCKERS
NOT_READY_HIGH_IMPACT_GAPS
PARTIAL_RESUMABLE
```

## 10. Review a patch against the baseline

Do not merge patch behavior into canonical current-system memory before it is current source.

Recommended sequence:

```text
Use /resume-reverse-engineering.
Use /patch-impact-review for <diff>.
```

If a requirement/specification exists:

```text
Use /requirement-compliance-review for <requirement> against <diff>.
```

Then derive tests:

```text
Use /regression-test-design for the reviewed change.
```

## 11. Produce a technical design

After the relevant current behavior is verified:

```text
Use /technical-design-proposal for <feature/change>.
```

The design must distinguish current verified behavior from proposed behavior and assumptions. Structural changes require current and proposed static architecture/class/component diagrams; significant runtime changes require flow/sequence diagrams.

## 12. After source changes are merged/current

First detect whether the stored baseline drifted:

```text
Use /architecture-drift-detection.
```

Then safely update canonical memory:

```text
Use /baseline-source-of-truth-maintenance.
```

Supersede stale evidence; do not erase history.

## 13. Canonical vs operational files

Canonical current-system knowledge:

```text
00_current_understanding.md
00_master_decision_matrix.md
```

Evidence lifecycle/history:

```text
00_evidence_ledger.md
```

Operational/non-canonical working memory:

```text
00_hypotheses.md
00_open_questions.md
00_workflow_state.md
00_investigation_coverage.md
```

Only promoted, verified current-system claims belong in canonical files.

## 14. Stop conditions

Stop and report `PARTIAL_RESUMABLE` when context/time is exhausted but the work can continue from repository state.

Report `NOT_READY_HIGH_IMPACT_GAPS` when important source-resolvable gaps remain.

Use `BASELINE_READY_WITH_EXTERNAL_BLOCKERS` only when the remaining high-impact facts genuinely require evidence unavailable in the repository, and each blocker names that evidence precisely.

## 15. What not to do

Do not:

- infer architecture from class names, subsystem names, protocol labels, or comments alone;
- use one test as proof of active production wiring;
- convert repeated AI statements into evidence;
- silently widen a claim from one operation/model/mode to all operations/models/modes;
- call an unknown external before exhausting source-visible configuration and binding paths;
- overwrite canonical baseline with an unmerged patch or proposed design;
- hide contradictions by deleting old evidence instead of superseding/rejecting it;
- load every generated artifact into context when a compact baseline plus targeted source is enough.
