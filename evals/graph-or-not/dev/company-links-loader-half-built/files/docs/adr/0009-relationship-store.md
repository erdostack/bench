# ADR 0009: relationships move to Neo4j

**Status:** accepted · **Date:** 2026-01-20 · **Deciders:** Halima, Stefan, Ngozi

## Context

registerlens is about connections. From the discovery interviews we expect users to follow ownership
and directorship chains four to six steps out ("who is really behind this company"), and to ask how two
entities are connected. In PostgreSQL each step is another self-join on `links`, and we do not expect
that to hold beyond two levels at 20 million rows.

## Decision

Keep entities and search in PostgreSQL. Move `links` into Neo4j and serve the links endpoint and the
connection finder from it.

## Consequences

- A loader and an ongoing sync from PostgreSQL (see `graph/`).
- A second datastore to run, back up and page for.
- Launch goes out on PostgreSQL; cutover follows once the loader is done.
