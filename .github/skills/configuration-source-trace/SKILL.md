---
name: configuration-source-trace
description: Trace behavior-changing configuration from its external/source definition through loader, key/default/override precedence, runtime state, consumer branch, and resulting behavior; use to close configuration-origin unknowns.
license: MIT
---

# Configuration Source Trace

## Mission

Answer precisely:

```text
Where does this configuration value come from?
How is it overridden?
How does it reach runtime behavior?
```

## Required Trace

For each material setting:

```text
source
→ file/env/system property/DB/CLI/default
→ key/schema
→ loader/parser
→ validation/conversion
→ precedence/override
→ runtime object/state
→ consumer
→ branch/selection
→ behavioral effect
```

## Search Strategy

Search from BOTH ends:

### Consumer backward

```text
branch/getter/field
→ assignment
→ constructor/setter/config object
→ loader
→ external source/key
```

### Source forward

```text
key/property/env/schema
→ parser
→ config object
→ consumer
→ runtime behavior
```

Inspect:

- property/yaml/json/xml files
- environment variables
- system properties
- command-line args
- DB-backed settings
- config defaults/constants
- profiles/overlays
- startup/bootstrap
- tests showing override precedence

## Required Findings

| Setting | External Source | Key | Default | Override Precedence | Loader | Runtime Holder | Consumer | Behavioral Effect | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|

Status:

```text
VERIFIED
PARTIALLY_VERIFIED
EXTERNALLY_INJECTED
NOT_APPLICABLE
UNRESOLVED
```

## External Values

If the actual deployed VALUE is unavailable but source proves the injection mechanism, separate:

```text
configuration mechanism = VERIFIED
runtime deployed value = EXTERNALLY_BLOCKED
```

Do not mark the entire configuration architecture UNKNOWN.

## Counterexample Search

Search for:

- duplicate keys
- deprecated keys
- alternate loaders
- profile-specific overrides
- defaults that bypass external configuration
- DB/runtime overrides
- test-only configuration

## Output

Create/update:

```text
docs/reverse-engineering/configuration/<scope>.md
```

Update open questions/evidence ledger as appropriate.
