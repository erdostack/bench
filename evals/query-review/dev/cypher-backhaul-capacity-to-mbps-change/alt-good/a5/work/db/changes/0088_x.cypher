MATCH ()-[l:BACKHAUL WHERE l.capacityKbps IS NOT NULL]->()
CALL (l) {
  SET l.capacityMbps = l.capacityKbps / 1000.0, l.capacityKbps = null
} IN TRANSACTIONS OF 10000 ROWS;
