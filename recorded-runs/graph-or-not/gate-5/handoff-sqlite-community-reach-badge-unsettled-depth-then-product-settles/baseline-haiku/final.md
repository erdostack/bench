Decision: keep follows in SQLite, do not move them to Neo4j for the badge

The badge only ever shows 1 or 2 steps, so it needs a two-step lookup on the follow table, not a graph traversal of arbitrary depth. At 9 ms p95 for that lookup on a copy of the database, SQLite meets the need with room to spare. Moving follows to Neo4j would add a second store and sync work to solve a problem that is not there.

The numbers it rests on:
- Two-step lookup on a copy of the database: 9 ms p95 (your timing; I could not reproduce it here, because the repo has no data or benchmark script).
- Badge depth: 1 or 2 only, as settled by Dana and the PM.
- Schema support: `follow` has primary key `(follower_id, followed_id)` and index `follow_followed (followed_id, follower_id)`, so both directions of a one-hop lookup are indexed.

Caveats before this is final:
- The 9 ms p95 is a timing on one copy. The repo does not say which sample of members or follow counts it used. The worst case for a two-step lookup is a well-connected viewer, so check the p95 across high-follow members, not only a typical sample.
- The badge is not built yet. `commons/profile.py` has only a TODO ("you're N introductions away"), so the timed query does not exist in the repo yet. Once it is written, the query itself should be checked against the 9 ms figure.
- The TODO does not say which direction "follows you" means. It should be stated before the query is written, so that the 1-step and 2-step cases match what Dana and the PM agreed.

Where it is written down: the decision record is not in this repository. The only trace here is the TODO in `commons/profile.py`, which describes the badge but does not record the decision, so I did not edit anything. Whoever keeps the decision record should add this entry with the 9 ms figure and the caveats above.
