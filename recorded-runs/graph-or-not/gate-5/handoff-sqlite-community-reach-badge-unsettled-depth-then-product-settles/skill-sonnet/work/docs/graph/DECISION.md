# Graph decision

Decision: recursive-sql

Product wants a "you're N introductions away" badge on member profiles, and Jonas wants the follow graph in Neo4j for it. Dana and the PM have settled the depth: the badge shows only 1 ("follows you") or 2 ("friend of a friend") and nothing further, which is a fixed two-step walk along `follow` between members. That walk was timed on a copy of the database at 9 ms p95 against the 150 ms the badge gets, so the SQLite database already run is enough and Neo4j is not needed.

## Workload facts

- 380,000 members and 6.4M follow rows, indexed both ways in the SQLite database (stated by the user; db/schema.sql: primary key (follower_id, followed_id) plus index `follow_followed` on (followed_id, follower_id))
- Profile views peak at about 70 a second (stated by the user)
- The badge gets 150 ms of the page (stated by the user)
- Depth is settled: the badge only ever shows 1 ("follows you") or 2 ("friend of a friend"), nothing further (stated by the user; agreed by Dana in growth and the PM). Earlier, Dana wanted up to 6 and the PM at most 2; the 6-step case is withdrawn.
- Measured: the two-step lookup on a copy of the database takes 9 ms p95 (stated by the user). Headroom to the budget = 150 / 9 = about 16.7 times.
- Jonas wants to move follows into Neo4j (stated by the user)
- The question asked: whether the viewer is 1 or 2 follow steps from the profile's member, a walk of fixed depth 2 along `follow` between members, not yet written (TODO in commons/profile.py). A short fixed walk is recursive-sql territory (self-joins or a recursive query on the SQLite database), not a plain join through a link table.
- The profile page today runs two single-row lookups and a count by `followed_id` (commons/profile.py)
- Average fan-out: 6.4M / 380,000 = 16.8 follows per member (derived from the stated counts). The median and the tail (hubs) are unknown
- Rows a two-step walk can reach: about 16.8 at 1 step and 16.8^2 = about 283 at 2 steps from one side (derived upper bound from the average fan-out); a meeting in the middle is smaller still. The required set is small, which is consistent with the 9 ms measurement.
- Load at peak: 70 views a second x 9 ms = about 0.63 s of query time a second if every view ran the walk at the p95 time on one connection; the mean is lower than the p95, and SQLite in WAL mode lets readers run side by side (derived; README.md)
- Operated today: Python 3.12, Starlette, SQLite in WAL mode on the app server, replicated with Litestream (README.md)
- unknown: whether the 9 ms p95 was timed under the 70-a-second peak load and for hub members, or one query at a time; only the user's figure exists, with no log or plan in the repo
- unknown: whether a step follows the arrow only (viewer follows ... follows member) or either way; the TODO says "through follows", and the badge text "follows you" suggests the arrow matters. Either way is about twice the edges walked
- unknown: what the badge shows when no 1- or 2-step connection exists, and whether a stale or cached answer is acceptable
- unknown: the follow write rate, the number of app-server processes, memory per process, and the tail fan-out; nothing in the repo states them
- unknown: the query plan; no database file is in the repo and I ran nothing

## Options considered

- graph-database (Neo4j, as Jonas proposes): rejected, because the walk is fixed at 2 steps and measured at 9 ms p95 against 150 ms on SQLite; Neo4j would be a second store holding the follow data, with a feed from the app database to keep in step with it, for no gain on a need that is already met.
- in-process-library (edges loaded into memory): rejected, because nothing is failing; 6.4M edges would be a copy per app-server process with its own reload, and the 2-step lookup already meets the budget.
- recursive-sql (a fixed two-step walk on the SQLite database already run, using the `follow` primary key for the forward step and `follow_followed` for the backward step): chosen, because it is measured at 9 ms p95 against 150 ms, over a required set of about 283 rows by average fan-out. Nothing needs to change in the database, so no new index or store is added.
- no-graph (plain joins, no traversal): rejected, because the badge walks the follow relation between members for 2 steps, and one step is only the "follows you" case, so the badge needs the second.

## What would change the decision

- The badge asked to show more than 2 steps (for example Dana's earlier up-to-6 case coming back) would reopen this; a walk deeper than 2 would need timing on the real follow data, including hub members, before any rung is chosen, and the PM and Dana set that depth.
- The two-step lookup measured over 150 ms p95 on production data at the 70-views-a-second peak (including hubs, and with the direction rule settled) would move this off recursive-sql; the cheaper remedies are one query per profile view and the existing indexes, and only if those fail would in-process-library or graph-database be considered.
- A badge latency budget below 150 ms, set by the product owner, would need the 9 ms figure checked against it.
