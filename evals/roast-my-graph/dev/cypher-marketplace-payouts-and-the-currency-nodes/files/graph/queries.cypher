// name: record_payment
MATCH (s:Seller {id: $seller})
MATCH (c:Currency {code: $currency})
CREATE (p:Payment {id: $id, amount_minor: $amount, at: datetime()})
CREATE (p)-[:FOR_SELLER]->(s)
CREATE (p)-[:IN_CURRENCY]->(c)
RETURN p.id;

// name: payment_receipt
MATCH (p:Payment {id: $id})-[:IN_CURRENCY]->(c:Currency)
RETURN p.id, p.amount_minor, c.code, c.minor_units, c.symbol;

// name: seller_balance
MATCH (s:Seller {id: $seller})<-[:FOR_SELLER]-(p:Payment)-[:IN_CURRENCY]->(c:Currency)
WHERE NOT (p)-[:PAID_OUT_IN]->(:Payout)
RETURN c.code, c.minor_units, sum(p.amount_minor) AS pending_minor;

// name: payout_lines
MATCH (o:Payout {id: $payout})<-[:PAID_OUT_IN]-(p:Payment)-[:IN_CURRENCY]->(c:Currency)
RETURN p.id, p.amount_minor, c.code, c.minor_units
ORDER BY p.id;

// name: create_payout
MATCH (s:Seller {id: $seller})<-[:FOR_SELLER]-(p:Payment)-[:IN_CURRENCY]->(c:Currency {code: $currency})
WHERE NOT (p)-[:PAID_OUT_IN]->(:Payout)
WITH s, c, collect(p) AS pending, sum(p.amount_minor) AS total
CREATE (o:Payout {id: $payout_id, total_minor: total, at: datetime()})-[:TO_SELLER]->(s)
FOREACH (p IN pending | CREATE (p)-[:PAID_OUT_IN]->(o))
RETURN o.id, total, c.code;
