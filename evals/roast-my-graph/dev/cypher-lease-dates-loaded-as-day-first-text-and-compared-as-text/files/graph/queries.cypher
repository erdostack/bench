// name: expiring_leases
MATCH (b:Building {code: $building})<-[:IN]-(u:Unit)<-[:FOR]-(l:Lease)<-[:HOLDS]-(t:Tenant)
WHERE l.ends >= $from AND l.ends <= $to
RETURN l.id AS lease, u.code AS unit, t.ref AS tenant, l.ends AS ends
ORDER BY l.ends;

// name: rent_roll_on
MATCH (l:Lease)-[:FOR]->(u:Unit)-[:IN]->(b:Building)
WHERE l.starts <= $day AND l.ends >= $day
RETURN b.code AS building, count(l) AS leases, sum(l.monthly_rent) AS rent
ORDER BY b.code;

// name: tenant_history
MATCH (t:Tenant {ref: $tenant})-[:HOLDS]->(l:Lease)-[:FOR]->(u:Unit)
RETURN l.id AS lease, u.code AS unit, l.starts AS starts, l.ends AS ends, l.monthly_rent AS monthly_rent
ORDER BY l.starts DESC;

// name: unit_card
MATCH (u:Unit {code: $unit})-[:IN]->(b:Building)
OPTIONAL MATCH (u)<-[:FOR]-(l:Lease)
RETURN u.code AS unit, b.code AS building, u.floor AS floor, u.rooms AS rooms, u.area_m2 AS area_m2,
       count(l) AS leases_so_far;
