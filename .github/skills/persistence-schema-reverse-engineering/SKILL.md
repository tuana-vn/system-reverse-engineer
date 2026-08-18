---
name: persistence-schema-reverse-engineering
description: Reconstruct persistence architecture and database/data schema from current source, ORM mappings, SQL, migrations, DDL, schema bootstrap, upgrade scripts, and runtime repository wiring; distinguish code-known schema from external-only details.
license: MIT
---

# Persistence and Schema Reverse Engineering

## Mission

Determine whether persistence exists, how code reaches it, and what schema/data model is actually supported by repository evidence.

## Applicability Check

First search for:

- JDBC/data sources/connections
- ORM entities/mappings
- repository/DAO classes
- SQL/query builders
- migration frameworks/scripts
- DDL/schema files
- embedded/test DB setup
- upgrade/install scripts
- table/column constants

If no persistence is materially present, record `NOT_APPLICABLE` with evidence and stop.

## Runtime Trace

Trace representative reads and writes:

```text
business/service
→ repository/DAO
→ ORM/query/SQL
→ connection/data source
→ table/entity/schema
```

Verify runtime binding of repository implementations when abstractions exist.

## Schema Reconstruction

Use evidence in priority order:

1. active migrations/DDL/schema bootstrap
2. active ORM/entity mappings
3. production SQL/query definitions
4. install/upgrade scripts
5. tests/test schema as supporting evidence only
6. docs/comments as secondary evidence

Reconstruct where supported:

- table/entity names
- important columns/fields
- data types
- PK/unique keys
- FKs/relationships
- indexes when behaviorally relevant
- read/write ownership
- transaction boundaries
- migration/version history

Do not invent missing columns or relationships.

## Required Tables

### Persistence Path

| Operation | Service/Caller | Repository/DAO | Concrete Binding | Query/ORM | Data Source | Evidence |
|---|---|---|---|---|---|---|

### Schema Inventory

| Table/Entity | Key | Important Fields | Relationships | Read By | Written By | Definition Evidence | Confidence |
|---|---|---|---|---|---|---|---|

### Schema Gaps

| Question | Search Performed | Code-Known Facts | Missing External Fact | Closure State |
|---|---|---|---|---|

## External Schema

If the repository contains queries/mappings but not authoritative DDL:

- promote only the schema facts directly required/proven by active code
- mark unavailable authoritative DDL/version as external if repository search is exhausted
- do not call all database schema details UNKNOWN

## Output

Create/update:

```text
docs/reverse-engineering/persistence/<scope>.md
```

Update evidence ledger/open questions as appropriate.
