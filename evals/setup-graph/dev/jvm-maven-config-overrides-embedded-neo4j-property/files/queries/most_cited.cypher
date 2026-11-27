MATCH (p:Paper)<-[:CITES]-(c:Paper)
RETURN p.title AS title, count(c) AS cited_by
ORDER BY cited_by DESC LIMIT 20;
