"""What drains into a node, for the flooding desk. Rule: the trace stops at pumping stations."""

UPSTREAM = """
WITH RECURSIVE up(node_id) AS (
    SELECT ?
    UNION
    SELECT p.us_node
    FROM pipe p
    JOIN up ON p.ds_node = up.node_id
    JOIN node n ON n.node_id = p.us_node
    WHERE n.kind <> 'pumping_station'
)
SELECT node_id FROM up WHERE node_id <> ? ORDER BY node_id
"""


def upstream_manholes(conn, node_id):
    return [r[0] for r in conn.execute(UPSTREAM, (node_id, node_id))]
