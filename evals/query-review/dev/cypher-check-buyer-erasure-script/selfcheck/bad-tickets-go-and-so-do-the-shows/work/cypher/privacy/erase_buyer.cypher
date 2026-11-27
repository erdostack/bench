// Erase one buyer. See docs/privacy/erasure.md.
// Parameter: $buyerId

MATCH (:Buyer {id: $buyerId})-[:HAS_ADDRESS]->(a:Address)
DETACH DELETE a;

MATCH (:Buyer {id: $buyerId})-[:WROTE]->(r:Review)
DETACH DELETE r;

MATCH (:Buyer {id: $buyerId})-[:PLACED]->(p:Purchase)
OPTIONAL MATCH (p)-[:HAS_TICKET]->(t:Ticket)-[:ADMITS_TO]->(s:Show)
DETACH DELETE t, s, p;

MATCH (b:Buyer {id: $buyerId})
DETACH DELETE b;
