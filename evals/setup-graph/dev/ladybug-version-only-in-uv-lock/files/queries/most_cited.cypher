MATCH (p:Paper)<-[:CITES]-(citing:Paper)
RETURN p.key AS key, count(citing) AS cited_by
ORDER BY cited_by DESC, key
LIMIT 5;
