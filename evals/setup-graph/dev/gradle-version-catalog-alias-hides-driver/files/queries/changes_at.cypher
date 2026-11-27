// Piers where you can change from route $route to another route, with the shortest wait.
MATCH (:Route {code: $route})-[:CALLS_AT]->(p:Pier)<-[:CALLS_AT]-(other:Route)
WHERE other.code <> $route
RETURN p.name AS pier, collect(DISTINCT other.code) AS routes
ORDER BY pier;
