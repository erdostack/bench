// Shortest relay chain from every buoy to any shore station.
MATCH (b:Buoy)
MATCH p = shortestPath((b)-[:RELAYS_TO*..12]->(:Station))
RETURN b.code AS buoy, length(p) AS hops
ORDER BY hops DESC, buoy;
