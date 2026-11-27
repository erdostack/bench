CYPHER 25
// Papers cited by at least three papers that cite each other, but cited by nobody outside that group.
MATCH (p:Paper)<-[:CITES]-(c:Paper)
WITH p, collect(c) AS citers
WHERE size(citers) >= 3
RETURN p.doi AS paper, size(citers) AS citers
ORDER BY citers DESC;
