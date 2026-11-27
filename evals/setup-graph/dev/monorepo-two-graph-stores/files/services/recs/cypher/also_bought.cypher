// Products most often in the same order as product 'SKU-1042'.
MATCH (p:Product {sku: 'SKU-1042'})<-[:CONTAINS]-(:Order)-[:CONTAINS]->(other:Product)
WHERE other <> p
RETURN other.sku AS sku, count(*) AS together
ORDER BY together DESC
LIMIT 10;
