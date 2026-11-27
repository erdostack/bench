MATCH ()-[l:BACKHAUL]->()
WHERE l.capacityKbps IS NOT NULL
CALL {
  WITH l
  SET l.capacityMbps = l.capacityKbps / 1000.0
  REMOVE l.capacityKbps
} IN TRANSACTIONS OF 10000 ROWS;
