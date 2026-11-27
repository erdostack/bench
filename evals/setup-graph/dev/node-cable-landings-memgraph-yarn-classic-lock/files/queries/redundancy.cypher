// Landing stations in $country and how many distinct cables land at each.
MATCH (s:Station)-[:IN]->(:Country {iso: $country})
OPTIONAL MATCH (c:Cable)-[:LANDS_AT]->(s)
RETURN s.name AS station, count(DISTINCT c) AS cables
ORDER BY cables, station;
