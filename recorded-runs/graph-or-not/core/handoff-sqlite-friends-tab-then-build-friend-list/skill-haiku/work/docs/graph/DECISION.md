# Graph decision

Decision: no-graph

The question is whether the Friends tab (a member's friends and when each friendship started, newest first, with closed accounts left out) needs a graph database, an in-memory graph library, recursive SQL or no graph at all, at about 20 page views a second at peak with about 12,000 members and 160,000 friendships. The answer is no-graph: the tab is a one-step lookup across the friendship link table, filtered by account state and sorted by start date, with no traversal beyond one step. The finding it turns on is that the query reads one hop of the friendship table, which is two indexed lookups (one per side of the pair) and a join to the account state.

## Workload facts

- The question asked of the connections: the direct friends of one member, each with the start date of the friendship (queries/ and hearth/profile.py; friends_tab is still the TODO, so no query runs today). This is one hop, not a walk: the link table is read once for the member, on both sides of the pair.
- Depth: 1 (derived from the request: "the member's friends").
- Account-closure rule (stated by the user, from legal's account-closure policy): a friend whose account has closed is never listed; all other states show, suspended accounts included.
- Account states in db/schema.sql and var/hearth.db (measured by reading the account_state table): 1 active, 2 closed, 3 suspended, 4 pending verification. The rule maps to the label 'closed'; the query should join on the label, not hard-code the code, since the table is the source of the labels (schema comment).
- Size (stated by the user): about 12,000 members and 160,000 friendships. Mean friends per member = 2 x 160,000 / 12,000 = 26.7 (derived).
- Sample in var/hearth.db (measured by count): 420 members, 1,700 friendships, mean 8.1 friends per member; 46 closed, 37 suspended, 5 pending verification, 332 active. The sample was used only for its schema and state labels, since its size is far below production.
- Load: the tab is opened about 20 times a second at peak (stated by the user).
- Measured, SQLite 3.53.1 and Python 3.13.18, on a synthetic copy at the stated size (12,000 members, 160,000 friendships, states drawn from the sample's mix, not production data):
  - query plan: both friendship sides use indexes (the primary key on person1_id and the index person_knows_person_2 on person2_id), member lookups in the person table use the primary key, and the only sort is a temporary B-tree over about 24 rows;
  - 600 random members: mean 23.9 friends listed, maximum 43; p50 0.054 ms, p99 0.137 ms, maximum 0.568 ms, one connection, warm cache;
  - a Python reference on one member matched the query exactly, and the result contained only states 1 and 3, with no closed account.
- Load arithmetic (derived from the measurement above): 20 views a second x 0.137 ms (p99) = 0.003 cores busy at peak.
- Start dates: creation_date is stored as TEXT in ISO format (YYYY-MM-DDTHH:MM:SS), length 19 for every friendship in the sample (measured), so ordering on the text sorts newest first correctly.
- unknown: the production state mix (the sample's closed share is 46 of 420 = 11%, which may differ from production).
- unknown: the production SQLite version and whether the copy is read from a replica; timings here are a warm, local, single-connection measurement.
- Operated today: one SQLite database (README.md); Python 3.11+, standard library only (README.md). No graph store in the repo.
- History: no earlier attempt at the Friends tab in the repo and no decision record.

## Options considered

- graph-database (a dedicated graph store; Bo proposed moving friendships into Neo4j): rejected, because the tab reads one hop of the friendship table and no query walks further. "A friends list is a graph query" holds only in the sense that the data can be drawn as a graph; the workload is a lookup across a link table once (measured p99 0.137 ms here). Neo4j would add a second store to keep in step with the closure rule, and it would not answer anything the existing query does not.
- in-process-library (friendships loaded into memory and a graph library): rejected, because nothing needs a traversal and the existing lookup already meets the load with a wide margin; loading a copy would add a reload step and a second source for the closure rule.
- recursive-sql (recursive queries on the existing database): rejected as unnecessary, because the question is one step deep; a recursive query would add nothing over the two indexed lookups already in the query.
- no-graph (plain joins, no traversal): chosen. The query is an indexed lookup of one member's friendships on both sides, a join to the person and account_state tables, a filter on the state label and a sort. It meets the requirement on the existing indexes.

## What would change the decision

- A request for friends of friends or any depth above one (for example mutual-friend chains or "how you're connected") would be a walk and would need the rung check again.
- A measured production run of the query showing a p99 well above the budget at 20 views a second, with the indexes in place and the data on the replica, would be the trigger to revisit the storage, not the graph model.
- The closure rule changing to hide suspended accounts or to hide friendships of a closed viewer would change the filter, not the model; it stays one hop.

Nothing in the repo was changed except this file, docs/graph/DECISION.md. hearth/profile.py is still the TODO. The scratch database used for the measurement was removed.
