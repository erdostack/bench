// Depots that can service every component fitted to a bogie type.
MATCH (b:Bogie {type: $type})-[:FITTED_WITH]->(c:Component)
WITH b.type AS type, collect(DISTINCT c) AS parts
MATCH (d:Depot)
WHERE all(p IN parts WHERE (d)-[:SERVICES]->(p))
RETURN d.name AS depot ORDER BY depot;
