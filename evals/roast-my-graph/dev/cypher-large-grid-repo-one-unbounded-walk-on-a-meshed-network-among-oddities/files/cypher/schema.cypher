CREATE CONSTRAINT zone_code IF NOT EXISTS FOR (z:Zone) REQUIRE z.code IS UNIQUE;
CREATE CONSTRAINT asset_tag IF NOT EXISTS FOR (a:Asset) REQUIRE a.tag IS UNIQUE;
CREATE CONSTRAINT meter_mpan IF NOT EXISTS FOR (m:Meter) REQUIRE m.mpan IS UNIQUE;
CREATE CONSTRAINT customer_id IF NOT EXISTS FOR (c:Customer) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT work_order_id IF NOT EXISTS FOR (w:WorkOrder) REQUIRE w.id IS UNIQUE;

// used by the label_* statements in ingest/assets.cypher
CREATE INDEX asset_kind IF NOT EXISTS FOR (a:Asset) ON (a.kind);
