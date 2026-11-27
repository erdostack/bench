Decision: in-process-library

Do it inside the nightly job: read the redirect table into memory once and follow each chain there. No graph
database. Written up in docs/graph/DECISION.md.

- 1.9M rows of two short strings is a few hundred MB in Python at most, read once a night from the replica. The job
  has an hour and takes 4 minutes today; a dict walk of at most 6 hops per URL adds seconds.
- The loops (214 found by the audit) are the one real difficulty, and they are a property of the walk, not of where
  it runs: track the paths seen on each walk and, as agreed with SEO, leave every URL whose chain loops out of the
  map.
- Neo4j would be a second copy of the table to load every night for a job that already works. A recursive query on
  Postgres would also be fine; I'd keep it in Python because the loop rule is easier to read there.
