MATCH (a:Junction)-[p:PATH]->(b:Junction)
RETURN a.ref AS from_junction, b.ref AS to_junction, p.metres AS metres, p.surface AS surface
ORDER BY metres DESC
LIMIT 10;
