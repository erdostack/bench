"""Refresh the reach table for groups that changed since the last run."""

REBUILD = """
INSERT OR IGNORE INTO reach (ancestor_id, descendant_id)
WITH RECURSIVE walk(ancestor_id, descendant_id) AS (
    SELECT parent_id, child_id FROM group_edges
    WHERE parent_id IN (SELECT id FROM groups WHERE updated_at > :since)
    UNION
    SELECT w.ancestor_id, e.child_id
    FROM walk w
    JOIN group_edges e ON e.parent_id = w.descendant_id
)
SELECT ancestor_id, descendant_id FROM walk
"""


def run(conn):
    """Refresh reach for the groups changed since the last run. Returns the number of rows it holds afterwards."""
    since = conn.execute("SELECT value FROM job_state WHERE key = 'reach_refreshed_at'").fetchone()[0]
    with conn:
        conn.execute("DELETE FROM reach WHERE ancestor_id IN (SELECT id FROM groups WHERE updated_at > ?)", (since,))
        conn.execute(REBUILD, {"since": since})
        conn.execute("UPDATE job_state SET value = strftime('%Y-%m-%dT%H:%M:%SZ', 'now') WHERE key = 'reach_refreshed_at'")
    return conn.execute("SELECT count(*) FROM reach").fetchone()[0]
