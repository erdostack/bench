# Writing queries

- The server is 2026.08 and 2026.x creates databases with Cypher 25 as the default, so queries are written in
  Cypher 25 and need no `CYPHER` prefix.
- Read-only queries only in `queries/`; the loader in `src/main/java/org/orchard/Load.java` is run by the survey
  lead after each season.
- Keep one statement per file. `scripts/q.sh` runs a file and prints the rows.
