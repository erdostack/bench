Decision: graph-database

The traces are walks up to 25 levels deep over 2.3 billion links in both directions, with a 30-second contract.
Postgres was tuned and still needs 14 minutes; memory is out (19 GB for a 1% sample against 64 GB hosts); the
graph database trial did 1.2 s and 0.9 s on a full copy and kept up with 3,000 writes a second. I've written
the decision and the numbers to docs/graph/DECISION.md.
