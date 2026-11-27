// Pairs of cultivars grafted onto the same rootstock.
MATCH (a:Cultivar)-[:GRAFTED_ON]->(r:Cultivar)<-[:GRAFTED_ON]-(b:Cultivar)
WHERE a.code < b.code
RETURN r.code, a.code, b.code ORDER BY r.code;
