// 1. substations and feeders
LOAD CSV WITH HEADERS FROM 'file:///feeders.csv' AS row
MERGE (s:Substation {id: row.substation_id})
MERGE (f:Feeder {id: row.feeder_id})
  SET f.name = row.feeder_name, f.voltage_kv = toFloat(row.kv)
MERGE (s)-[:SUPPLIES]->(f);

// 2. transformers, with the feeder(s) that can supply them
LOAD CSV WITH HEADERS FROM 'file:///transformers.csv' AS row
CALL (row) {
  MERGE (t:Transformer {id: row.transformer_id})
    SET t.kva = toInteger(row.kva),
        t.upstream_ids = split(row.feeder_ids, ';')
} IN TRANSACTIONS OF 10000 ROWS;

// 3. meters, with the transformer that supplies them
LOAD CSV WITH HEADERS FROM 'file:///meters.csv' AS row
CALL (row) {
  MERGE (m:Meter {id: row.meter_id})
    SET m.address = row.address,
        m.upstream_ids = [row.transformer_id]
} IN TRANSACTIONS OF 10000 ROWS;
