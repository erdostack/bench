MATCH (p:Person)-[:LEADS]->(t:Team)
RETURN t.name AS team, p.fullName AS lead
ORDER BY team;
