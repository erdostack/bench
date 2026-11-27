MATCH (a:Plant)<-[:VISITED]-(p:Pollinator)-[:VISITED]->(b:Plant)
WHERE id(a) < id(b)
RETURN a.name, b.name, count(p) AS shared ORDER BY shared DESC LIMIT 20;
