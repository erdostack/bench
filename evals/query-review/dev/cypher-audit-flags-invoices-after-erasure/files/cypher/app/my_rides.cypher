// Ride history in the app.
// Parameters: $riderId
// Returns: id, startedAt, fromDock, toDock
MATCH (:Rider {id: $riderId})-[:TOOK]->(r:Ride)-[:FROM]->(f:Dock), (r)-[:TO]->(t:Dock)
RETURN r.id AS id, r.startedAt AS startedAt, f.name AS fromDock, t.name AS toDock
ORDER BY startedAt DESC
LIMIT 100;
