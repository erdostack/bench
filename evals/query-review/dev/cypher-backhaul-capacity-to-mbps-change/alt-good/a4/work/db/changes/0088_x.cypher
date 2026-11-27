MATCH ()-[l:BACKHAUL]->()
CALL (l) {
  SET l.capacityMbps = coalesce(l.capacityMbps, l.capacityKbps / 1000.0)
  REMOVE l.capacityKbps
} IN TRANSACTIONS OF 10000 ROWS;
