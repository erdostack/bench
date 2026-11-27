// move. count: MATCH ... RETURN count(b);
MATCH (o:Performance {code: 'HAM-1128-E'}), (n:Performance {code: 'HAM-1214-M'})
CALL (o, n) {
  MATCH (p:Patron)-[b:BOOKED {status: 'confirmed'}]->(o)
  CREATE (p)-[:BOOKED {seat: b.seat, status: b.status, price: b.price, bookedAt: b.bookedAt}]->(n)
  DELETE b
} IN TRANSACTIONS OF 1 ROWS;
