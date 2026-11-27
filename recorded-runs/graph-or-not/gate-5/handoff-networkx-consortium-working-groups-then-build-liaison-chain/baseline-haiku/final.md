I added `liaison_chain(conn, a, b)` in `consortium/liaison.py`. It loads the membership graph with `consortium.graph.load_graph` and returns the shortest chain from organisation a to organisation b, as a list alternating organisation ids and working-group codes, e.g. `[1, 'WG-001', 2, 'WG-002', 3]`.

- It returns `[a]` when a and b are the same organisation.
- It returns `None` when no chain exists, when an id is not an organisation, or when an organisation has no memberships.

I tested it on a small in-memory SQLite database built from `db/schema.sql`. Cases covered: a direct shared group, a three-hop chain through two groups, the same organisation, an organisation with no memberships, an unknown id, and a working-group code passed in place of an organisation id. All returned the expected results.

Open points for you:
- Every membership counts as a link, whatever the role (including `observer`) and even when `meetings_per_year` is 0. The TODO says the rules still need to come from the secretary-general's office, so I did not filter on either field. If only active memberships should count, the filter goes in `load_graph` or before the graph is built.
- Chains are found by hop count, and when several chains tie, the result depends on row order in the database.
- The view and its route are not added, since you said you would do the view.
