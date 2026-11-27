Added `migrations/V023__backfill_object_accession_year.cypher`.

About 5.1 million objects need the year (docs/model.md), and docs/migrations.md caps a
transaction at 200,000 changed properties, so it runs in batches of 50,000 with
`CALL { } IN TRANSACTIONS`. That clause can't run inside the managed transaction that
tools/migrate.py uses by default, so the file starts with `// migrate: autocommit`, the runner's
switch for this. It only touches objects whose year is null and whose number starts with four
digits and a dot, and writes the year as an integer. It is safe to re-run if a deploy stops halfway.

Before the release, on the local copy: `EXPLAIN` the statement, and
`MATCH (o:Object) WHERE o.accessionYear IS NULL RETURN count(o)` before and after.
