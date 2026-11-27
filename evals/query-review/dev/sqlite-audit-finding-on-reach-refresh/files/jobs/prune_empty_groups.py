"""Remove groups that have no nestings in either direction and were not touched for a year."""


def run(conn):
    with conn:
        cur = conn.execute(
            "DELETE FROM groups WHERE updated_at < date('now', '-1 year') "
            "AND id NOT IN (SELECT parent_id FROM group_edges) AND id NOT IN (SELECT child_id FROM group_edges)")
    return cur.rowcount
