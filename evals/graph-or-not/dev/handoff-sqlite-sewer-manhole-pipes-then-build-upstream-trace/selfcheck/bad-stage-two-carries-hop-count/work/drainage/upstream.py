UPSTREAM = """
WITH RECURSIVE up(node_id, hops) AS (
    SELECT ?, 0
    UNION
    SELECT p.us_node, up.hops + 1
    FROM pipe p
    JOIN up ON p.ds_node = up.node_id
    JOIN node n ON n.node_id = p.us_node
    WHERE n.kind <> 'pumping_station'
)
SELECT DISTINCT node_id FROM up WHERE node_id <> ? ORDER BY node_id
"""


def upstream_manholes(conn, node_id):
    return [r[0] for r in conn.execute(UPSTREAM, (node_id, node_id))]
