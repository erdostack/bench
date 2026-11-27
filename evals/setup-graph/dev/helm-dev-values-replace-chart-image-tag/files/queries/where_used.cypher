// Assemblies that contain $part at any depth, with the quantity needed per assembly.
MATCH path = (a:Assembly)-[:CONTAINS*1..8]->(p:Part {sku: $part})
RETURN a.sku AS assembly,
       length(path) AS depth,
       reduce(q = 1, c IN relationships(path) | q * c.quantity) AS quantity
ORDER BY depth, assembly
