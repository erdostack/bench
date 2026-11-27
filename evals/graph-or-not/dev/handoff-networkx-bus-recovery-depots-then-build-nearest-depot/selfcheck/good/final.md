Rewrote nearest_depot in recovery/nearest.py, per docs/graph/DECISION.md: segments with bus_gate = 1 are left
out (the truck is a lorry), the rest go into a MultiGraph so a road beside a bus gate is kept, and Dijkstra on
minutes picks the depot. Returns (depot_id, minutes), or None when no depot can reach the junction.
