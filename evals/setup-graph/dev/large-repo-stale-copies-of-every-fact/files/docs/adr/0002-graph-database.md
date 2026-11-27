# ADR 2: Store the collection as a graph

Status: accepted (2022)

## Context

Provenance is a chain: made by, sold to, bequeathed to, acquired by, lent to. The registrar's questions follow
those chains to an unknown depth. The relational prototype needed a new recursive query for every question.

## Decision

Use Neo4j. We standardise on Neo4j 4.4 LTS with the official Python driver (`pip install neo4j==4.4.*`), and
keep every query in a `.cypher` file so that the registrar can read them.

## Consequences

- One more service to run.
- Queries are reviewed like code.
- We accept a single writer (the nightly import) and treat the database as read-mostly.
