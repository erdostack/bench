Added connection_degree(conn, viewer_id, owner_id) to profiles/connection.py.

It follows the rule in docs/graph/DECISION.md: the number of friendship steps from the viewer to the owner, 0 on
your own profile, and -1 when the owner is more than 3 steps away or not connected at all. Friendships are stored
once per pair, so each step goes both ways. One bounded recursive query on SQLite.
