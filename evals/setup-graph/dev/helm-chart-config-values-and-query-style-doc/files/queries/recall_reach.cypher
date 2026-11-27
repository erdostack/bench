// Which retailers can a recalled lot have reached?
MATCH (l:Lot {code: $lot})-[:BOTTLED_BY]->(p:Producer)
MATCH (p)-[:SHIPS_TO]->(d:Distributor)-[:SUPPLIES*1..3]->(r:Retailer)
LET region = r.region
RETURN DISTINCT r.name, region
ORDER BY region, r.name;
