# Nightly scores: where they run

Decision: in-process-library

## Workload facts (from the owner)

- About 210,000 accounts and 2.8 million follows; the export is about 60 MB.
- Batch box: 8 GB of RAM. The job starts at 02:30 and must be done by 06:00.
- Trust & safety: a muted follow passes no reach (not an in-link, not counted in the follower's following) but
  still links the two accounts for rings.
- Definitions: docs/scores.md (reach = 20 PageRank steps, d = 0.85; ring = accounts joined by follows either way).
- Export columns: followed_id, follower_id, muted (header line of follows.edges).

## Options considered

- graph-database (Priya: Neo4j and its algorithm plugin): rejected, a server and a nightly import for two batch
  algorithms that fit in memory.
- in-process-library: chosen, NetworkX is already in requirements.txt.
- recursive-sql: no SQL store holds the export.
- no-graph: no; both scores are whole-graph computations.

## What would change the decision

- Scores needed during the day as follows change, or an export that outgrows the 8 GB box.
