# V3.0 Notes

## Why V3.0

V2.1 could finish `/full-reverse-engineering` while still reporting HIGH-impact unknowns. It also emphasized verification governance so strongly that source exploration could become too conservative.

V3.0 changes the methodology from:

```text
discover → verify/promote → audit → consolidate
```

to:

```text
aggressive discovery
→ evidence hardening
→ high-impact unknown closure
→ adversarial coverage/readiness audit
→ consolidate
```

## Major Changes

1. **Discovery and certification are explicitly separated.**
2. **HIGH/CRITICAL unknown closure is mandatory before readiness.**
3. Added explicit readiness states instead of ambiguous `COMPLETE`.
4. Added investigation coverage tracking.
5. Added configuration provenance tracing.
6. Added runtime-binding verification.
7. Added persistence/database-schema reverse engineering.
8. Added completeness/coverage audit.
9. `/full-reverse-engineering` no longer blindly limits representative flows to 3–5 when more distinct architecture paths exist.
10. Final baseline includes config/runtime binding/persistence/lifecycle/coverage, not only runtime flow + integration boundaries.

## New Skills

```text
/resolve-high-impact-unknowns
/configuration-source-trace
/runtime-binding-verification
/persistence-schema-reverse-engineering
/reverse-engineering-coverage-audit
```

## Readiness Gate

```text
BASELINE_READY
```

requires zero unresolved source-resolvable HIGH/CRITICAL gaps and no HIGH/CRITICAL coverage gap.

If remaining high-impact facts genuinely require evidence outside the repository:

```text
BASELINE_READY_WITH_EXTERNAL_BLOCKERS
```

and each blocker must name the exact missing external evidence.

## Public-release cleanup

- moved agent/skills/instructions to GitHub-supported project locations under `.github/`;
- removed repository-specific protocol/product vocabulary from global instructions;
- removed `incident-root-cause-analysis` and `observability-traceability-analysis` from the focused public package;
- removed the redundant nested README from the resume skill;
- added README, operational runbook, security guidance, and MIT license;
- retained patch/compliance/test/design workflows because they are direct consumers of the verified reverse-engineering baseline.
