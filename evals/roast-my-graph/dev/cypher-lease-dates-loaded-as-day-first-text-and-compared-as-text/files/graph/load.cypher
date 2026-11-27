// name: load_units
UNWIND $rows AS row
MERGE (b:Building {code: row.building_code})
MERGE (u:Unit {code: row.unit_code})
SET u.floor = toInteger(row.floor),
    u.rooms = toInteger(row.rooms),
    u.area_m2 = toInteger(row.area_m2)
MERGE (u)-[:IN]->(b);

// name: load_leases
UNWIND $rows AS row
MATCH (u:Unit {code: row.unit_code})
MERGE (t:Tenant {ref: row.tenant_ref})
MERGE (l:Lease {id: row.lease_id})
SET l.starts = row.starts,
    l.ends = row.ends,
    l.monthly_rent = toInteger(row.monthly_rent)
MERGE (t)-[:HOLDS]->(l)
MERGE (l)-[:FOR]->(u);
