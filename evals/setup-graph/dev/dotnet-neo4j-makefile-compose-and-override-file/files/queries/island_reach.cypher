// Islands reachable from one port with at most two changes of ferry.
MATCH (start:Port {code: $port})-[:SAILS_TO*1..3]->(p:Port)
WHERE p <> start
RETURN DISTINCT p.island AS island
ORDER BY island;
