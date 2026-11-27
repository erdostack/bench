// name: upsert_cables
UNWIND $rows AS row
MATCH (a:Asset {tag: row.from_tag})
MATCH (b:Asset {tag: row.to_tag})
MERGE (a)-[c:CONNECTS {cable_id: row.cable_id}]->(b)
SET c.normally_open = row.normally_open, c.length_m = row.length_m;

// name: remove_cables
// cables the register no longer lists
UNWIND $rows AS row
MATCH (a:Asset {tag: row.from_tag})-[c:CONNECTS {cable_id: row.cable_id}]->(:Asset)
DELETE c;

// name: upsert_supply
// A meter hangs off exactly one transformer; moving it replaces the old link.
UNWIND $rows AS row
MATCH (t:Asset:Transformer {tag: row.transformer_tag})
MERGE (m:Meter {mpan: row.mpan})
SET m.phase = row.phase
WITH t, m
OPTIONAL MATCH (other:Transformer)-[old:SUPPLIES]->(m)
WHERE other <> t
DELETE old
WITH DISTINCT t, m
MERGE (t)-[:SUPPLIES]->(m);
