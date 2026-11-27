"""Rebuild the reach table from group_edges."""

REBUILD = """
INSERT INTO reach (ancestor_id, descendant_id)
WITH RECURSIVE walk(ancestor_id, descendant_id) AS (
    SELECT parent_id, child_id FROM group_edges
    UNION
    SELECT w.ancestor_id, e.child_id
    FROM walk w
    JOIN group_edges e ON e.parent_id = w.descendant_id
)
SELECT ancestor_id, descendant_id FROM walk
"""


def run(conn):
    """Replace the content of reach. Returns the number of rows it holds afterwards."""
    while True:
        cur = conn.execute("DELETE FROM reach WHERE (ancestor_id, descendant_id) IN "
                           "(SELECT ancestor_id, descendant_id FROM reach LIMIT 5000)")
        conn.commit()
        if cur.rowcount == 0:
            break
    with conn:
        conn.execute(REBUILD)
        conn.execute("UPDATE job_state SET value = strftime('%Y-%m-%dT%H:%M:%SZ', 'now') WHERE key = 'reach_refreshed_at'")
    return conn.execute("SELECT count(*) FROM reach").fetchone()[0]
