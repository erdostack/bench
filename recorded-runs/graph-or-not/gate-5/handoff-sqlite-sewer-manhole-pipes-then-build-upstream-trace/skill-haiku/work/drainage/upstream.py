"""Upstream list for the flooding desk. conn is a sqlite3 connection to the sewer export (db/schema.sql)."""

# Walks backward along the pipes from node_id. A UNION on node_id alone stops the walk on the overflow
# pipes that are digitised in both directions. Pumping stations are never listed and never expanded,
# so nothing that drains only through one is listed either.
_UPSTREAM_SQL = """
WITH RECURSIVE up(node_id) AS (
    SELECT :node_id
    UNION
    SELECT p.us_node
    FROM up
    JOIN node u ON u.node_id = up.node_id AND u.kind <> 'pumping_station'
    JOIN pipe p ON p.ds_node = up.node_id
    JOIN node n ON n.node_id = p.us_node AND n.kind <> 'pumping_station'
)
SELECT node_id FROM up WHERE node_id <> :node_id ORDER BY node_id
"""


def upstream_manholes(conn, node_id):
    """Sorted ids of the nodes that drain into node_id, not including node_id or any pumping station.

    If node_id is itself a pumping station, the list is empty.
    """
    return [row[0] for row in conn.execute(_UPSTREAM_SQL, {"node_id": node_id}).fetchall()]
