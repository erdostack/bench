Decision: no-graph

At the depth the PM proposed (2 steps at most), the badge is two indexed lookups. It does not need a graph database, a graph library, or a recursive query. The Neo4j proposal should not go ahead for this feature. The one open question is the depth, and it changes the answer only if the team picks 6.

Why 2 steps is not a graph problem here:

- "Follows you" is one row: `follow` with `follower_id = member` and `followed_id = viewer`, or the reverse depending on direction. The primary key `(follower_id, followed_id)` answers it.
- "Friend of a friend" is one join. The viewer's follows (`follower_id = viewer`) intersected with the member's followers (`followed_id = member`). The existing `follow_followed` index serves the second side. Each side is bounded by the viewer's follow list, which at this graph's average (about 6.4M rows over 380k members, roughly 17 follows per member) is a few dozen to a few hundred ids.
- At 70 page views a second and a 150 ms budget, two indexed lookups fit comfortably in SQLite on the app server. I have not timed this on the real data. It is a reasoned estimate from the schema, and the first thing to confirm is `EXPLAIN QUERY PLAN` on real member ids.

Sketch for the PM's version (untested, for the design discussion; the direction must be settled first):

```sql
-- 1 step: the viewer follows the member
SELECT 1 FROM follow WHERE follower_id = :viewer AND followed_id = :member
UNION ALL
-- 2 steps: the viewer follows someone who follows the member
SELECT 2 FROM follow a JOIN follow b ON b.follower_id = a.followed_id
WHERE a.follower_id = :viewer AND b.followed_id = :member
LIMIT 1;
```

Decisions the meeting has to settle first:

- Direction. "You're N introductions away" can mean a directed path (viewer follows A, A follows member) or an undirected one (any follow in either direction). The sketch above is directed. Undirected means checking both directions and adds two more joins. Pick one before anyone writes the query.
- Whether "1 step" means follows-in-either-direction. That is the same question as the one above.

What changes if the team picks 6 steps (Dana's proposal):

- At this graph's density, a 6-step search can reach most of the 380k members from a single viewer. That is a breadth-first search over most of the network per page view, at 70 a second. A recursive SQL query with a visited set would do that work on every view, and I would not expect it to meet 150 ms. An in-memory graph of 6.4M edges would work for the search, but it is a new process and a new sync path for every follow, and that is a different decision from this one.
- The usual way to serve a deep badge at this volume is to precompute the distances. Either a cache keyed by viewer, refreshed in the background, or a bounded answer ("more than 2 steps" for anything beyond the 2-step window). Both are product trade-offs as much as technical ones. Neither is a reason to adopt a graph database for a 2-step badge.
- So the 6-step version is the case where a graph approach might be needed, and this report does not decide it. If the team goes to 6, re-run the decision with a timed breadth-first search on the real follow table.

Recommendation: build the 2-step badge with the two indexed queries above, on the existing SQLite database. Show the badge only for 1 or 2 steps, and show nothing (or "more than 2") beyond that. Settle the direction question first. Revisit the depth question with the product team before anyone proposes Neo4j for this feature.
