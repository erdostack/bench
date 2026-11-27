MATCH (s:Site)<-[:STOPPED_AT]-(r:Ringing)-[:OF]->(sp:Species)
RETURN s.name AS site, count(DISTINCT sp) AS species
ORDER BY species DESC LIMIT 15;
