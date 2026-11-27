// Depots with no route from the hub.
MATCH (hub:Depot {code: 'HUB'}), (d:Depot)
WHERE d <> hub AND NOT exists((hub)-[:LINK *BFS]->(d))
RETURN d.code AS depot
ORDER BY depot;
