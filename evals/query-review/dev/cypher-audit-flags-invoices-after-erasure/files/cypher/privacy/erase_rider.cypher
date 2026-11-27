// Erase one rider as described in docs/privacy/retention.md.
// Parameter: $riderId

// 1. Invoices are kept for tax, without the personal details on them.
MATCH (:Rider {id: $riderId})-[:BILLED]->(i:Invoice)
REMOVE i.billingName, i.billingEmail, i.billingAddress
SET i.anonymisedAt = datetime();

// 2. Rides, with their GPS traces.
MATCH (:Rider {id: $riderId})-[:TOOK]->(r:Ride)
DETACH DELETE r;

// 3. Payment cards.
MATCH (:Rider {id: $riderId})-[:HAS_CARD]->(c:PaymentCard)
DETACH DELETE c;

// 4. The account.
MATCH (x:Rider {id: $riderId})
DETACH DELETE x;
