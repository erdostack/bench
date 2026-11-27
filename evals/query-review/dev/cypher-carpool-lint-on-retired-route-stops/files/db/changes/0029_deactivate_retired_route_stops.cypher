// SR-114: stops of retired routes must stop showing on the drivers' map.
MATCH (r:Route)-[:FIRST_STOP]->(:Stop)-[:NEXT*0..]->(s:Stop)
WHERE r.retiredOn IS NOT NULL
CALL (s) {
  SET s.active = false
} IN TRANSACTIONS OF 5000 ROWS;
