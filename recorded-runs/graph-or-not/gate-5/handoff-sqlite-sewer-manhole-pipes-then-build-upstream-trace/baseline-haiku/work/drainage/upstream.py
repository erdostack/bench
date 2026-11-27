"""Upstream list for the flooding desk. conn is a sqlite3 connection to the sewer network export (db/schema.sql)."""

UPSTREAM_SQL = """
WITH RECURSIVE up(node_id) AS (
    SELECT us_node FROM pipe WHERE ds_node = :node_id
    UNION
    SELECT p.us_node FROM pipe AS p JOIN up ON p.ds_node = up.node_id
)
SELECT node_id FROM up WHERE node_id <> :node_id ORDER BY node_id
"""


def upstream_manholes(conn, node_id):
    """Sorted ids of every node that drains into node_id, directly or through other pipes.

    Follows every pipe kind as digitised (gravity, rising main, overflow). The node itself is not included.
    Tracks node ids only, not hop counts, so a cycle in the export (e.g. an overflow digitised both ways)
    terminates instead of looping.
    """
    return [row[0] for row in conn.execute(UPSTREAM_SQL, {"node_id": node_id})]
