// move. Count: MATCH ... RETURN count(b);
MATCH (p:Patron)-[b:BOOKED {status: 'confirmed'}]->(:Performance {code: 'HAM-1128-E'})
MATCH (n:Performance {code: 'HAM-1214-M'})
MATCH (q:Patron)
CALL (q, b, n) {
  CREATE (q)-[:BOOKED {seat: b.seat, status: b.status, price: b.price, bookedAt: b.bookedAt}]->(n)
  DELETE b
} IN TRANSACTIONS OF 500 ROWS;
