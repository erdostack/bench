# Production

Neo4j 5.20 Enterprise on every target (the 2026.x upgrade is scheduled for March 2027).

Changing production data: write the statement as a file in `ops/`, have a second engineer review it,
then the on-call runs it once with `bin/gq prod --file ops/<file>` (cypher-shell, auto-commit). Nobody
else sends writes to prod. Reads are fine.

Big changes run in batches of at most 20,000 rows per transaction: outage management reads the graph
around the clock.
