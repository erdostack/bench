// name: upsert_customers
UNWIND $rows AS row
MERGE (c:Customer {id: row.id})
SET c.name = row.name, c.priority = row.priority;

// name: upsert_holdings
UNWIND $rows AS row
MATCH (c:Customer {id: row.customer_id})
MATCH (m:Meter {mpan: row.mpan})
MERGE (c)-[h:HOLDS]->(m)
ON CREATE SET h.since_ms = row.since_ms;

// name: upsert_work_orders
// TODO(asset-team): closed orders older than seven years can go
UNWIND $rows AS row
MERGE (w:WorkOrder {id: row.id})
SET w.kind = row.kind, w.due_ms = row.due_ms, w.closed_ms = row.closed_ms
WITH w, row
MATCH (a:Asset {tag: row.asset_tag})
MERGE (w)-[:ON]->(a);
