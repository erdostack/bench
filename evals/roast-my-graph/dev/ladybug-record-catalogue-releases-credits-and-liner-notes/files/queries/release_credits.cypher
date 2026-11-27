MATCH (p:Person)-[c:CREDITED_ON]->(r:Release {id: $release_id})
RETURN p.id, p.name, c.role
ORDER BY c.role, p.name;
