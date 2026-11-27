"""Everything that drains into a node (docs/graph/DECISION.md: recursive-sql on the SQLite export)."""

UPSTREAM_SQL = """
WITH RECURSIVE up(node_id) AS (
    SELECT :node_id
  UNION
    SELECT p.us_node
    FROM up
    JOIN pipe AS p ON p.ds_node = up.node_id
    JOIN node AS n ON n.node_id = p.us_node
    WHERE n.kind <> 'pumping_station'
)
SELECT node_id FROM up WHERE node_id <> :node_id ORDER BY node_id
"""


def upstream_manholes(conn, node_id):
    """Sorted ids of the nodes that drain into node_id, not node_id itself.

    The trace stops at pumping stations: a station is not listed and the walk does not continue
    through it, so what drains only into a station (the pumping team's catchment) is left out.
    A node that also drains to node_id by a route avoiding every station is still listed.
    Rows are deduplicated on node id alone, so two-way overflow links (a cycle) terminate.
    If node_id is itself a pumping station, the walk still starts from it.
    """
    return [r[0] for r in conn.execute(UPSTREAM_SQL, {"node_id": node_id})]
