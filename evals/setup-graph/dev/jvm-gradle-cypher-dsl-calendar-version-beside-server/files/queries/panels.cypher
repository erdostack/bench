MATCH (a:Speaker)-[:SPEAKS_ON]->(t:Topic)<-[:SPEAKS_ON]-(b:Speaker)
WHERE a.handle < b.handle
RETURN a.handle, b.handle, collect(t.name) AS shared ORDER BY size(shared) DESC LIMIT 10;
