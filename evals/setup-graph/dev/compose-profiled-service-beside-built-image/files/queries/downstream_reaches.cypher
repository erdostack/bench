// Reaches downstream of reach $reach, in flow order.
MATCH path = (:Reach {id: $reach})-[:FLOWS_INTO*1..30]->(r:Reach)
RETURN r.id AS reach, length(path) AS steps
ORDER BY steps;
