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
    # SA-14: the DELETE has no WHERE on purpose. reach is derived from group_edges and is rebuilt in full by the
    # next statement, inside this one transaction, so readers see the old closure or the new one (docs/jobs.md).
    # Scoping it to groups whose updated_at moved would leave revoked paths behind: removing a nesting touches
    # only the parent, but every ancestor of the parent loses the path too.
    with conn:
        conn.execute("DELETE FROM reach")
        conn.execute(REBUILD)
        conn.execute("UPDATE job_state SET value = strftime('%Y-%m-%dT%H:%M:%SZ', 'now') WHERE key = 'reach_refreshed_at'")
    return conn.execute("SELECT count(*) FROM reach").fetchone()[0]
