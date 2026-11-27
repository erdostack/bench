Added connection_degree(conn, viewer_id, owner_id). The badge is capped at 2 steps ("friend" and "friend of a
friend"), so anything further returns -1, as does no path; your own profile is 0.
