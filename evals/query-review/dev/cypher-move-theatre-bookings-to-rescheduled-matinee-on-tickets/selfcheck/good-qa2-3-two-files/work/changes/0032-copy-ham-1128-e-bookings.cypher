// step 1: copy confirmed bookings HAM-1128-E to HAM-1214-M. Count: MATCH ... RETURN count(b);
MATCH (p:Patron)-[b:BOOKED {status: 'confirmed'}]->(:Performance {code: 'HAM-1128-E'})
MATCH (n:Performance {code: 'HAM-1214-M'})
CALL (p, b, n) {
  CREATE (p)-[:BOOKED {seat: b.seat, status: b.status, price: b.price, bookedAt: b.bookedAt}]->(n)
} IN TRANSACTIONS OF 500 ROWS;
