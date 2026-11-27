// Flattened parts list of $assembly.
MATCH path = (:Assembly {sku: $assembly})-[:CONTAINS*1..8]->(p:Part)
WITH p, sum(reduce(q = 1, c IN relationships(path) | q * c.quantity)) AS quantity
RETURN p.sku AS part, p.description AS description, quantity
ORDER BY part
