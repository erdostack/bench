MATCH (a:Site)-[l:BACKHAUL]->(b:Site)
WITH l WHERE l.capacityKbps IS NOT NULL
CALL (l) {
  SET l += {capacityMbps: toFloat(l.capacityKbps) / 1000.0, capacityKbps: null}
} IN TRANSACTIONS OF 10000 ROWS;
