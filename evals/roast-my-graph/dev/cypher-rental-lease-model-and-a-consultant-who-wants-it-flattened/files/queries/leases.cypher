// name: arrears
MATCH (l:Lease {status: 'active'})-[:FOR_UNIT]->(u:Unit)
WHERE l.start <= date() - duration('P90D')
OPTIONAL MATCH (p:Payment)-[:AGAINST]->(l)
WHERE p.paid_on >= date() - duration('P90D')
WITH l, u, coalesce(sum(p.amount_eur), 0) AS paid_90d
WHERE paid_90d < l.rent_eur * 3
RETURN u.address AS unit, l.id AS lease, paid_90d, l.rent_eur * 3 AS due_90d
ORDER BY unit;

// name: tenant_home
MATCH (t:Tenant {id: $tenant})-[:SIGNED]->(l:Lease)-[:FOR_UNIT]->(u:Unit)
OPTIONAL MATCH (d:Deposit)-[:HELD_FOR]->(l)
RETURN l.id AS lease, u.address AS unit, l.start AS start, l.end AS end, l.status AS status,
       d.amount_eur AS deposit
ORDER BY start DESC;

// name: record_payment
MATCH (l:Lease {id: $lease})
CREATE (p:Payment {id: $payment_id, amount_eur: $amount, paid_on: date($paid_on), payer: $payer})
CREATE (p)-[:AGAINST]->(l);
