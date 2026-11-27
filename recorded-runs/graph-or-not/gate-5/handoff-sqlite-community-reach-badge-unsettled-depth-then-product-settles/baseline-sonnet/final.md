Decision: no-graph

With the badge limited to 1 or 2, there is no graph problem left. Don't use Neo4j, a graph library or recursive SQL. Plain indexed lookups in the existing SQLite database are enough.

The numbers it rests on:
- The two-step lookup runs at 9 ms p95 on a copy of the database. The badge's budget is 150 ms, so it uses about 6% of it.
- The data is 380k members and 6.4M follow rows, indexed both ways in SQLite. The peak is about 70 profile views a second.
- Jonas's case for Neo4j was about a badge reaching up to 6 steps. With a 2-step limit, the search is bounded by how many people a member follows, and the existing indexes handle that. A second database would have to be run, synced with the SQLite source of truth and secured for one badge, and it would buy nothing measurable here.

What I changed:
- `sql/introductions.sql` (new): returns 1 if the viewer and member follow each other in either direction. It returns 2 if they share a connection, meaning someone one of them follows or is followed by who is also connected to the other. Otherwise it returns no row. No recursion.
- `commons/profile.py`: a new `introductions()` function calls that query, and `profile()` now returns an `"introductions"` field (1, 2 or `None`). The TODO is gone. Viewing your own profile gives `None`.
- `README.md`: a new "Decisions" section records the call, the 9 ms and 150 ms numbers, why Neo4j was rejected, and when to revisit it (only if the badge is ever extended past 2 steps, and then measure a bounded search on a copy of the real database first).

Checked on a small in-memory database built from `db/schema.sql`: direct follows in both directions give 1, friend of a friend gives 2, and three or more steps give `None`. I did not run it on a copy of the real database. The 9 ms figure is yours, from the timing you did of the two-step lookup, and I haven't confirmed that my query matches what you timed.

One thing to confirm with Dana and the PM: I treated "follows you" and "friend of a friend" as direction-independent, so a follow either way counts. If "follows you" should mean only that the member follows the viewer, or friend of a friend should mean only viewer to someone to member, tell me and I'll tighten the query. A narrower query is cheaper, so the timing would not get worse.
