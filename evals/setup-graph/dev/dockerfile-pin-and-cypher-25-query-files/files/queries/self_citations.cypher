CYPHER 25
MATCH (a:Author)-[:WROTE]->(p:Paper)-[:CITES]->(q:Paper)<-[:WROTE]-(a)
RETURN a.name AS author, count(*) AS self_cites
ORDER BY self_cites DESC;
