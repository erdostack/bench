// Erase one rider.
// Parameter: $riderId

MATCH (:Rider {id: $riderId})-[:BILLED]->(i:Invoice)
DETACH DELETE i;

MATCH (:Rider {id: $riderId})-[:TOOK]->(r:Ride)
DETACH DELETE r;

MATCH (:Rider {id: $riderId})-[:HAS_CARD]->(c:PaymentCard)
DETACH DELETE c;

MATCH (x:Rider {id: $riderId})
DETACH DELETE x;
