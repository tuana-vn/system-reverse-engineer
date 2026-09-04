# Runtime Artifact Naming Contract

## Principle

Generated filenames are intentionally short and stable.

Do NOT append:

- package version
- execution date
- timestamp
- run ID

to generated filenames.

Version, date, source commit, execution mode, and run identity belong in artifact metadata and the
run manifest, not in filenames.

## Run Isolation

Fresh runs remain isolated by directory:

```text
docs/reverse-engineering/runs/<run_id>/
```

The directory identifies the run. Files inside the directory use fixed names.

Example:

```text
docs/reverse-engineering/runs/audit_traceability/
├── RUN_MANIFEST.yaml
├── workflow_state.yaml
├── verification/
│   └── tdd_verification.md
├── design/
│   ├── design_artifact_registry.md
│   └── verification/
│       └── design_artifact_registry_verification.md
├── implementation/
│   ├── wbs.md
│   ├── wbs_verification.md
│   └── implementation_readiness.md
└── audits/
    └── post_readiness_audit.md
```

## Run Metadata

`RUN_MANIFEST.yaml` records:

```yaml
run_id:
agent_package_version:
workflow:
execution_mode:
source_commit:
started_at:
last_updated:
status:
artifacts:
```

The generated date/version is read from artifact metadata or the manifest.

## Latest Run

`docs/reverse-engineering/LATEST_RUN.md` remains a convenience pointer only.

It identifies the current run directory and manifest.

## Future Implementation Agent Naming

Implementation-agent outputs must also use stable filenames.

Recommended layout:

```text
docs/reverse-engineering/runs/<run_id>/implementation-results/
├── IMPL_MANIFEST.yaml
├── patch_summary.md
├── build_report.md
└── test_report.md
```

Do NOT append dates, package versions, run IDs, or implementation attempt IDs to these filenames.

If implementation history must be preserved, create a separate attempt directory:

```text
implementation-results/attempt-01/
implementation-results/attempt-02/
```

and keep the filenames inside each attempt directory unchanged.
