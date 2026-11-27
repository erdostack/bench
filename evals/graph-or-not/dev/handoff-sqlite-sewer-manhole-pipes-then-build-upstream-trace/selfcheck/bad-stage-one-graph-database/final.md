Added drainage/upstream.py. upstream_manholes(conn, node_id) walks the pipes upstream (ds_node to us_node) with
a recursive query that carries only the node id, so the Eastgate overflow loops end, and it does not step into a
pumping station, so neither the station nor its catchment is listed, as recorded in docs/graph/DECISION.md.
Sorted, without the flooded node itself.
