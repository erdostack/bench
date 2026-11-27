# Graph decision

Decision: no-graph

The Friends tab (a member's friends and when each friendship started, newest first, without closed accounts) should stay in SQLite as one ordinary query, not move to Neo4j. The tab reads a member's direct friends only, so it follows no relation for more than one step; at about 27 friends per member and 20 opens a second, one indexed join does the job.

## Workload facts

- The question: the member's direct friends with the friendship's creation date, newest first. One step from one member, no walk (request; hearth/profile.py is a TODO with no query yet).
- Production is about 12,000 members and 160,000 friendships (stated by the user).
- The tab is opened maybe 20 times a second at peak (stated by the user). Each open is an online request.
- Legal rule from the account-closure policy: a friend who has closed their account is never listed; everyone else shows, suspended accounts included, since they can come back (stated by the user). In `account_state` the codes are 1 active, 2 closed, 3 suspended, 4 pending verification (measured: `SELECT * FROM account_state` on var/hearth.db), so the filter is `state <> 2`, not `state = 1` and not the suspended code 3. A filter that listed only active members would hide suspended and pending members, which the rule says must show.
- Storage: one SQLite database `var/hearth.db`; the copy in `var/` is a sample with the same tables (README.md). Friendships are one row per pair `person_knows_person(person1_id, person2_id, creation_date)` with `person1_id < person2_id`, primary key (person1_id, person2_id) and index `person_knows_person_2(person2_id)`, so a lookup by either side is indexed (db/schema.sql). `person.state` references `account_state(code)`.
- Sample: 420 members (332 active, 46 closed, 37 suspended, 5 pending verification), 1,700 friendships, of which 339 involve a closed member, and at most 17 friends for one member (measured: read-only SQLite 3.53.1 queries on var/hearth.db).
- Average production fan-out: 2 x 160,000 / 12,000 = about 27 friends per member (derived from the stated numbers). The tail (hubs) is unknown.
- Candidate query measured on the sample: join `person_knows_person` to `person` on the other side of the friendship (an OR on the two id columns, `CASE` to pick the other member), filter `state <> 2`, order by `creation_date DESC`. It ran at about 0.04 ms per call over 500 random members, returning 7.3 rows on average. SQLite's plan used both indexes through MULTI-INDEX OR, a primary key lookup on `person`, and a temporary b-tree for the sort (measured: `EXPLAIN QUERY PLAN`).
- Load: 20 calls a second x 0.04 ms is far below one core's time (derived; the timing is from the sample, not production).
- Writes and freshness: unknown; the query reads the live database.
- unknown: production timing, the largest friend counts at production size, and whether a friend list is paged; none is in the repo or the request.

## Options considered

- graph-database (Neo4j, as Bo proposes): rejected, because the query reads one member's direct friends, which is a one-step lookup that two indexes already serve in about 0.04 ms on the sample; moving 160,000 friendships to a second store would not change the query and would add a feed that must also carry the account state the legal rule depends on. A friends list being drawn as a graph does not make it a traversal.
- in-process-library (friendships loaded into memory): rejected, because nothing in the question needs more than one step, and a copy per process would need reloading to keep up with the legal closure rule.
- recursive-sql: rejected, because there is no walk; a recursive query would be added where one join does the work.
- no-graph (plain SQL, one join with the person table): chosen, because the tab follows no relation for more than one step and the query meets the need on the sample. Write it in `queries/friends_tab.sql` with named parameters like `queries/profile_header.sql`, with `p.state <> 2`, ordered by `creation_date DESC` (ties by the friend's id for a stable order).

## What would change the decision

- A product change from a friends list to a "friends of friends" or "people you may know" tab, or any query that follows friendships for more than one step, would move this to recursive-sql and be tested again.
- A measured production-size 99th percentile for the Friends tab above its latency budget (the team that owns the page sets the budget, none is given) at the stated 20 opens a second would call for plan and index work on this query first, not a move to a graph store.
- A member with a very large friend count (check the largest counts with a `GROUP BY` over both columns of `person_knows_person`) that makes the list too long to show at once would need paging, not a graph.
- Closed accounts being tracked in a place other than `person.state` would change the filter, not the decision.
