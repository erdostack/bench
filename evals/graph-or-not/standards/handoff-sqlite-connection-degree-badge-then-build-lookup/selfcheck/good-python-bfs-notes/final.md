Added connection_degree(conn, viewer_id, owner_id) in profiles/connection.py, per notes/badge.md: a breadth-first
search over friend lists (both directions of knows), 0 for your own profile, -1 past 3 steps or with no path.
