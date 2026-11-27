MATCH (p:Person {id: $person_id})-[c:CREDITED_ON]->(r:Release)
RETURN r.id, r.title, r.year, c.role
ORDER BY r.year, r.title;
