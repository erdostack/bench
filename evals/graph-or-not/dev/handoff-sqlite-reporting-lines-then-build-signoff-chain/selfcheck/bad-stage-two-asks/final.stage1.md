Decision: recursive-sql

The sign-off chain is a walk of at most a dozen steps up the solid lines in a 3 MB SQLite file, so it stays in
SQLite. Written up in docs/graph/DECISION.md, with Finance's rules, so whoever builds it has them.

- Finance's rules: solid lines only (dotted-line leads never sign), start at the submitter's manager, stop at the
  first person at grade 7 or above and include them. With 23 loops in the export, the walk also stops when it
  comes back to someone already in the chain or to the submitter, and HR ops takes it from there.
- One WITH RECURSIVE query that carries the path answers it in well under a millisecond on 6,400 employees and
  7,900 reporting lines, and the page opens about 200 times a day.
- Neo4j would add a server and a sync from the hourly export for a lookup of at most 12 rows.
