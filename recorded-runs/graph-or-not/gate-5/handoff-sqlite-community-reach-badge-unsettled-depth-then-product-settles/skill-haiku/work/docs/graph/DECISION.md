# Graph decision

Decision: recursive-sql

Product asks whether the "you're N introductions away" badge on member profiles (the TODO in `commons/profile.py`) needs a graph database, an in-memory graph library, recursive SQL or no graph. The badge now shows only 1 or 2 steps, so a two-step lookup on the SQLite database already in use is the answer: 9 ms p95 on a copy of the database (stated by the user) against the 150 ms the badge gets, which is 16.7 times headroom (derived: 150 / 9). The earlier need-more-information verdict rested on the depth, and that depth is now settled at 2, so no move to Neo4j is needed.

## Workload facts

- 380k members and 6.4M follow rows (stated by the user; earlier record; `db/schema.sql` has the tables and the counts are not in the repo). Average follows per member: 6.4M / 380k = 16.8 (derived).
- Depth: the badge shows 1 step ("follows you") or 2 steps ("friend of a friend") and nothing further (stated by the user; settled by Dana and the PM). The earlier record had the depth open, with the PM wanting 2 and Growth wanting up to 6. The settled depth replaces both, so the up-to-6 case no longer applies.
- Two-step lookup, measured: 9 ms p95 on a copy of the database (stated by the user, timed by the user). The sample of viewers, the query text and whether the timing was single runs or under load are not stated.
- Budget for the badge: 150 ms (stated by the user; earlier record). Headroom against the 9 ms p95: 16.7 times (derived: 150 / 9).
- Peak load: about 70 profile views a second (stated by the user; earlier record). At 9 ms per lookup, 70 x 0.009 = 0.63 s of database time per second at peak, about 63% of one core (derived; assumes the 9 ms holds at peak concurrency, which is not measured).
- Index both ways: `follow` is `WITHOUT ROWID` with primary key `(follower_id, followed_id)` and an index `follow_followed (followed_id, follower_id)` (`db/schema.sql`). Out-edges of a viewer and in-edges of a member are both index-range scans.
- Earlier naive estimate, random graph and not measured: about 17 + 284 = 300 index lookups per view on average at 2 steps (derived from the branching estimate in the earlier record), about 21,000 a second at peak (derived: 300 x 70). Real follow graphs cluster, so this is an upper estimate and not a forecast.
- Hub tail: the largest follower count and follow count are unknown. A member with many followers makes the in-list scan longer. Whether the 9 ms sample included such members is unknown.
- Direction: "follows you" implies the badge depends on direction. The query shape that was timed is not stated. Both indexes are present, so either direction is index-served (`db/schema.sql`). Unknown whether the timed query used both sides.
- Current profile query: two indexed counts (`commons/profile.py`); its timing is not in the repo.
- Operated today: SQLite in WAL mode on the app server, replicated with Litestream (`README.md`). Memory per process and number of app processes: unknown.
- Write rate and freshness the badge needs: unknown.
- Measured here: nothing. `var/commons.db` is not committed, so the 9 ms figure could not be checked in this session (measured by the user, not here).

## Options considered

- graph-database (Jonas's proposal, Neo4j for follows): rejected. The badge is a fixed two-step walk, and the timed lookup meets 150 ms with 16.7 times headroom on SQLite. A second stateful store would add a sync for a query that already meets its budget.
- in-process-library (a graph library with the follow list in memory): rejected. Loading 6.4M follow rows into each process for a lookup that takes 9 ms in SQL is more machinery than the badge needs.
- recursive-sql (a fixed two-step walk as a two-sided self-join on the SQLite database already run): chosen. It meets the need at 9 ms p95 against 150 ms (stated by the user), with both indexes in place, and needs no new system and no recursion beyond two steps.
- no-graph (plain joins): rejected as a description. The friend-of-a-friend answer follows the same relation twice, so it is a short walk. Written as self-joins it is the recursive-sql rung above, which is still plain SQL.

## What would change the decision

- The depth the badge shows grows beyond 2 (a product decision for Dana and the PM). At 3 steps or more the reach is no longer bounded by the naive estimate and must be measured again. At up to 6 steps the reach approaches the whole graph, and the choice would move to graph-database or in-process-library, picked by measurement.
- The 2-step p95 measured under load on the real follow table exceeds 150 ms at 70 views a second, including the members with the most followers in the sample. Then the rung fails, and the hub tail is measured first (the maximum follower and follow counts, read from a copy of `var/commons.db` opened read-only), before any graph store is considered.
- The timed query is not the two-sided lookup the badge will run, or the sample left out the largest-follower members. Run the production query and a sample that includes hubs on a copy, read-only, with `EXPLAIN QUERY PLAN`.
- The 9 ms figure does not hold on the production hardware at production load. Owner: the platform team, with Jonas.
