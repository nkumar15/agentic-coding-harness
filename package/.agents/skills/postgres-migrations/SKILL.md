---
name: postgres-migrations
description: Design and implement PostgreSQL schema migrations using the migration style declared by project conventions. Use when adding or changing PostgreSQL tables, indexes, constraints, RLS, temporal history, or seed/reference data.
license: Proprietary
compatibility: Host-neutral repository workflow
metadata:
  author: Neeraj
  version: "2.0"
---

# PostgreSQL Migrations Skill

Use this skill when `.agents/rules/project-conventions.md` says the project uses PostgreSQL.
Project conventions are the source of truth for migration tool, directory layout, naming, required
columns, tenant model, temporal/history model, seed data, and verification commands.

## Migration Shape

- Use the repository's declared migration mechanism: SQL files, Alembic, Flyway, Liquibase, Django
  migrations, or another project-defined tool.
- Every schema change must be reversible unless project conventions explicitly allow irreversible
  migrations with human approval.
- Keep migrations small, ordered, and named according to project conventions.
- Separate schema changes from data backfills when that reduces deploy risk.

## Tables And Columns

- Use project-defined required columns for identifiers, audit fields, timestamps, tenant keys, soft
  delete, temporal ranges, and ownership metadata.
- Use timezone-aware timestamps when the project does not define another standard.
- Prefer `NOT NULL` when the business meaning of missing data is not defined.
- Use constraints for invariant business rules that must hold regardless of application path.

## Indexes And Constraints

- Index foreign keys and high-selectivity query/filter columns used by the feature.
- Include tenant or partition keys in indexes when project conventions require tenant-scoped access.
- Avoid indexes that are not justified by a query path, uniqueness rule, or gate evidence.
- Prefer check constraints or lookup tables for stable enumerations, following project conventions.

## Multi-Tenancy And RLS

- Apply Row-Level Security only when project conventions require database-enforced tenant isolation.
- If RLS is used, define policies, grants, admin/app roles, and tenant-context setup exactly as the
  project conventions specify.
- Do not manually duplicate tenant filtering in application code unless that is the project pattern.
- Tests must prove tenant isolation when the feature touches tenant-scoped data.

## Temporal Or History Tables

- Add history, audit, soft-delete, or temporal behavior only when project conventions require it for
  the table type.
- If the project uses system-period temporal tables, keep main/history schema, triggers, grants, and
  query patterns consistent with existing migrations.
- Do not invent a second history mechanism for tables already governed by a project standard.

## Seed And Reference Data

- Treat seed data as part of the contract when the feature depends on it.
- Keep test seed data separate from demo or local-only seed data unless project conventions state
  otherwise.
- Add rollback or cleanup behavior for seed changes where feasible.

## Verification

- Run migration apply and rollback checks from `.agents/process/gates.yaml` or project conventions.
- Add tests for schema-backed behavior in the same change as application code.
- Record known limitations, irreversible steps, and required deploy sequencing in the architecture or
  PR evidence.
