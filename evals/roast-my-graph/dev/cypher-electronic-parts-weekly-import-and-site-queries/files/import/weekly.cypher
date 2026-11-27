// name: import_parts
UNWIND $rows AS row
MERGE (p:Part {mpn: row.mpn})
SET p.title = row.title, p.updated = date()
MERGE (p)-[:MADE_BY]->(m:Maker {name: row.maker});

// name: import_offers
UNWIND $rows AS row
MATCH (p:Part {mpn: row.mpn})
MERGE (d:Distributor {code: row.distributor})
MERGE (p)-[o:OFFERED_BY]->(d)
SET o.price = row.price, o.stock = row.stock, o.seen = date();
