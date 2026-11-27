"""Everything that drains into a node, by recursive SQL on the monthly export."""

# UNION (not UNION ALL) on node_id alone is what ends the walk on loops, such as the two-way overflow
# links on Eastgate: a node already reached is never expanded again. Do not add a hop counter to the
# CTE columns; it makes every revisit a new row and the query never finishes on a cycle.
# Pumping stations are not entered, so neither they nor anything upstream of them (reached only
# through them) is returned.
UPSTREAM_SQL = """
WITH RECURSIVE up(node_id) AS (
    SELECT :node_id
    UNION
    SELECT p.us_node
    FROM pipe p
    JOIN up ON p.ds_node = up.node_id
    JOIN node n ON n.node_id = p.us_node
    WHERE n.kind <> 'pumping_station'
)
SELECT n.node_id, n.asset_ref, n.kind, n.catchment
FROM up JOIN node n ON n.node_id = up.node_id
WHERE up.node_id <> :node_id
ORDER BY n.asset_ref
"""


def upstream_manholes(conn, node_id):
    """Rows (node_id, asset_ref, kind, catchment) draining into node_id, stopping at pumping stations."""
    start = conn.execute("SELECT kind FROM node WHERE node_id = ?", (node_id,)).fetchone()
    if start is None or start[0] == "pumping_station":
        return []
    return conn.execute(UPSTREAM_SQL, {"node_id": node_id}).fetchall()
