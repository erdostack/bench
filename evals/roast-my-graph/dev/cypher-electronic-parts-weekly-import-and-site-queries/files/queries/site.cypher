// name: maker_directory
MATCH (m:Maker)<-[:MADE_BY]-(p:Part)
RETURN m.name AS maker, count(p) AS parts
ORDER BY maker;

// name: maker_page
MATCH (m:Maker {name: $maker})<-[:MADE_BY]-(p:Part)
RETURN p.mpn AS mpn, p.title AS title
ORDER BY mpn
SKIP $offset LIMIT 50;

// name: part_offers
MATCH (p:Part {mpn: $mpn})-[o:OFFERED_BY]->(d:Distributor)
WHERE o.seen >= date() - duration('P8D')
RETURN d.code AS distributor, o.price AS price, o.stock AS stock
ORDER BY price;
