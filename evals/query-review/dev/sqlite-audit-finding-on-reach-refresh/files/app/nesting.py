"""Changing which group is nested in which."""


class WouldLoop(ValueError):
    pass


def _now(conn):
    return conn.execute("SELECT strftime('%Y-%m-%dT%H:%M:%SZ', 'now')").fetchone()[0]


def add_nesting(conn, parent_id, child_id):
    """Nest child in parent. Refuses a nesting that would make a group contain itself."""
    loops = conn.execute(
        """WITH RECURSIVE below(id) AS (
               SELECT ? UNION SELECT e.child_id FROM below b JOIN group_edges e ON e.parent_id = b.id)
           SELECT 1 FROM below WHERE id = ?""", (child_id, parent_id)).fetchone()
    if loops:
        raise WouldLoop(f"group {parent_id} is already inside group {child_id}")
    now = _now(conn)
    with conn:
        conn.execute("INSERT INTO group_edges (parent_id, child_id, added_at) VALUES (?, ?, ?)", (parent_id, child_id, now))
        conn.execute("UPDATE groups SET updated_at = ? WHERE id = ?", (now, parent_id))


def remove_nesting(conn, parent_id, child_id):
    """Take child out of parent."""
    now = _now(conn)
    with conn:
        conn.execute("DELETE FROM group_edges WHERE parent_id = ? AND child_id = ?", (parent_id, child_id))
        conn.execute("UPDATE groups SET updated_at = ? WHERE id = ?", (now, parent_id))
