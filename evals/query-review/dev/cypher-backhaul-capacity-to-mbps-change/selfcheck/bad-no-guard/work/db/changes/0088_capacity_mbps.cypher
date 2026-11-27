MATCH ()-[l:BACKHAUL]->()
CALL (l) {
  SET l.capacityMbps = toFloat(l.capacityKbps) / 1000
  REMOVE l.capacityKbps
} IN TRANSACTIONS OF 10000 ROWS;
