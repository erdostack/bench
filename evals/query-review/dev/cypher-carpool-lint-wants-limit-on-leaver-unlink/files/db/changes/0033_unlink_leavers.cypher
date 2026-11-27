// SR-140: children who have left the district come off every carpool list.
MATCH (s:Student)-[m:RIDES_IN]->(:Carpool)
WHERE s.leftOn IS NOT NULL
CALL (m) {
  DELETE m
} IN TRANSACTIONS OF 4000 ROWS;
