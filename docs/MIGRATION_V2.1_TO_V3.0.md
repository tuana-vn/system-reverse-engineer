# Upgrade from V2.1 to V3.0

## Recommended for an existing repository with V2.1 baseline

Do NOT delete existing `docs/reverse-engineering/` evidence history.

Install the V3.0 `copilot-home` files, then run in Copilot:

```text
/agent
→ system-reverse-engineer
```

Then:

```text
Use /resume-reverse-engineering.
Then run /resolve-high-impact-unknowns for all existing HIGH/CRITICAL open questions.
Then run /reverse-engineering-coverage-audit.
Then continue /full-reverse-engineering from the V3.0 readiness phases instead of restarting from scratch.
```

## Clean rerun

If you intentionally want to rebuild the baseline from zero, archive/remove the old generated `docs/reverse-engineering/` workspace first and run:

```text
Use /full-reverse-engineering.
```

Do not mix old canonical claims into a supposedly clean baseline without re-verification.
