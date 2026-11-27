// Stops within two stops of this one, for the "nearby" panel.
MATCH (s:Stop {id: $id})-[:LINK*1..2]-(n:Stop)
WHERE n <> s
RETURN DISTINCT n.id AS id, n.name AS name
ORDER BY name;
