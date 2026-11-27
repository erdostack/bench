// Stop pairs that need more than two changes.
MATCH (a:Stop {zone: 1}), (b:Stop {zone: 4})
MATCH p = shortestPath((a)-[:NEXT*..60]-(b))
RETURN a.name AS from, b.name AS to, length(p) AS legs
LIMIT 50;
