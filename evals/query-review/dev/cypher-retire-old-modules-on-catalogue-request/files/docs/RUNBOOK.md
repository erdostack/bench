# Runbook

## Targets

- `dev`: Neo4j 2026.10 in Docker on your machine, with the sample catalogue loaded.
- `catalogue`: production (Neo4j 2026.10 Enterprise). The public module finder, programme approval and
  the exam timetabler read it. The name comes from the Course Catalogue project that first built it.

## Changing data on catalogue

A change to data on `catalogue` is a file `changes/<ticket>-<what>.cypher` whose header comment gives the
ticket, what changes and how many nodes it should touch. Another engineer reviews it in a pull request,
and the curriculum-systems on-call runs it with `bin/modq catalogue --file changes/<file>`. Nobody else
writes to `catalogue`.

A statement that writes more than 10,000 rows is batched with `CALL { ... } IN TRANSACTIONS OF n ROWS`,
n at most 10,000.
