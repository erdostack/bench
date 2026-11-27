MATCH (p:Person {id: $person_id})-[:CREDITED_ON]->(r:Release)<-[:CREDITED_ON]-(other:Person)
WHERE other.id <> p.id
RETURN other.id, other.name, count(DISTINCT r) AS releases_together
ORDER BY releases_together DESC
LIMIT 25;
