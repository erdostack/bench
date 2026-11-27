MERGE (c:Collection {slug: 'gifts-under-50'}) ON CREATE SET c.title = 'Gifts under €50';
MATCH (c:Collection {slug: 'gifts-under-50'}), (b:Bundle {status: 'live'}) WHERE b.priceCents < 5000
MERGE (b)-[:IN_COLLECTION]->(c);
