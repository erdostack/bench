// Retailers per distributor, for the quarterly report
MATCH (d:Distributor)-[:SUPPLIES]->(r:Retailer)
WITH d, count(r) AS retailers
WHERE retailers > 0
RETURN d.name, retailers
ORDER BY retailers DESC;
