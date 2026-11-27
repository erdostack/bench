// Longest feeding chain ending at each top predator.
MATCH path = (top:Species)-[:EATS*1..6]->(base:Species)
WHERE NOT EXISTS { (:Species)-[:EATS]->(top) } AND NOT EXISTS { (base)-[:EATS]->(:Species) }
RETURN top.name AS predator, max(length(path)) AS longest_chain
ORDER BY longest_chain DESC;
