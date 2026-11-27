Decision: no-graph

You don't need Neo4j, a graph library or recursive SQL for this. "Can this viewer see this profile" is one hop through the membership table: the viewer's current teams, the subject's current teams, and a check for a shared team with at most 40 current members. Nothing is walked to a variable depth.

The numbers it turns on:
- Size: 41,000 membership rows, about 6,000 ended, so 35,000 current (about 3.8 teams per person). The database is about 6 MB, and team_member is already indexed on both person_id and team_id.
- Load: 50 views a minute is under one a second.
- Measured: I built a synthetic SQLite database of that size (including an 8,900-person company team) and ran the check for 2,000 random pairs. Mean 1.7 ms, worst 12.3 ms. It is random data, not your real database, so treat it as order of magnitude.

How to build it (I did not change any code): for the DPO rule, count members only where left_at IS NULL, keep teams with a count of 40 or less, and allow the profile if the viewer and the subject both have a current row in one of those teams. Ended memberships must be excluded from the size count as well as from membership; that is the easy one to get wrong.

Not found: whether a person can always see their own profile (the rule doesn't say), the real distribution of team sizes near the 40 cap, and how often owners edit teams. Neither Neo4j nor an in-memory copy would help with these. A copy would also go stale against owner edits, which is not good for a privacy rule.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
