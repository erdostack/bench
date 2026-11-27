Added connection_degree(conn, viewer_id, owner_id) to profiles/connection.py, following docs/graph/DECISION.md:
steps from the viewer along knows, 0 for your own profile, -1 past 3 steps or with no path.
