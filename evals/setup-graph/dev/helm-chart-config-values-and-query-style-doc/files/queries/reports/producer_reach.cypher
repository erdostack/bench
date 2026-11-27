// Distinct retailers each producer reaches
MATCH (p:Producer)-[:SHIPS_TO]->(:Distributor)-[:SUPPLIES]->(r:Retailer)
RETURN p.name, count(DISTINCT r) AS retailers
ORDER BY retailers DESC;
