---
name: runtime-binding-verification
description: Prove how an abstraction, interface, mode, or configured choice becomes the concrete runtime implementation actually used, including DI/bootstrap/factory/provider/registry and alternate branches.
license: MIT
---

# Runtime Binding Verification

## Mission

Close the gap between:

```text
"an implementation exists"
```

and:

```text
"this implementation is actually selected under these runtime conditions"
```

## Start From

One high-impact abstraction, selector, factory, client, repository, handler, or mode whose active implementation matters.

## Trace

Trace both directions where needed:

```text
startup/bootstrap
→ registration / DI / provider / registry
→ selector/factory
→ config/runtime state
→ concrete implementation
→ real caller/use
```

and:

```text
runtime caller
→ abstraction
→ creation/lookup
→ concrete instance
→ boundary
```

## Search

Inspect as applicable:

- constructors and `new`
- dependency injection annotations/config
- service loaders/plugins
- factories/providers/builders
- registries/maps
- startup/main/application initialization
- reflection/class-name loading
- configuration mode switches
- test-only bindings vs production bindings
- legacy/inactive implementations
- fallback implementations

## Counterexample Search

Search for every implementation and every creation/registration path of the abstraction.

Do not conclude from one call site.

## Output

Create/update:

```text
docs/reverse-engineering/runtime-binding/<scope>.md
```

Required table:

| Scope/Condition | Abstraction | Binding Mechanism | Concrete Implementation | Config/Runtime Input | Active Evidence | Alternate Binding | Verdict |
|---|---|---|---|---|---|---|---|

Verdict:

```text
VERIFIED_ACTIVE
VERIFIED_ALTERNATE
INACTIVE_LEGACY
TEST_ONLY
UNRESOLVED
```

Promote only after counterexample search and scope check.
