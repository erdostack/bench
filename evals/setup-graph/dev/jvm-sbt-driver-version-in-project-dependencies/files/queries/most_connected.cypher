MATCH (m:Musician)-[:PLAYED_ON]->(:Session)<-[:PLAYED_ON]-(other:Musician)
RETURN m.name AS musician, count(DISTINCT other) AS partners
ORDER BY partners DESC LIMIT 10;
