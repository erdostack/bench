MATCH (t:Team)-[:OWNS]->(s:Service)
RETURN t.name AS team, count(s) AS services
ORDER BY services DESC, team;
