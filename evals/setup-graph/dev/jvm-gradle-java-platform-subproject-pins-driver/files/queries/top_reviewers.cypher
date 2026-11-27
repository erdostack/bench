MATCH (r:Person)-[:REVIEWED]->(c:Change)
RETURN r.login AS reviewer, count(c) AS reviews ORDER BY reviews DESC LIMIT 10;
