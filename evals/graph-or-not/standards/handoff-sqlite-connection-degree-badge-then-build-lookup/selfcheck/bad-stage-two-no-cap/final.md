Added connection_degree(conn, viewer_id, owner_id) to profiles/connection.py: a breadth-first search over friend
lists in both directions, returning the number of steps, 0 for yourself and -1 when there is no path.
