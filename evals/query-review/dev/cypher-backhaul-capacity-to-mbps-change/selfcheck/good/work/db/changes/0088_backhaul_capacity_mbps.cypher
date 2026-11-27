// NET-311: capacityKbps (INTEGER) -> capacityMbps (FLOAT).
// Safe to retry: only links that still have capacityKbps are converted, and the old property is
// removed in the same batch as the new one is written.
MATCH ()-[l:BACKHAUL]->()
WHERE l.capacityKbps IS NOT NULL
CALL (l) {
  SET l.capacityMbps = l.capacityKbps / 1000.0
  REMOVE l.capacityKbps
} IN TRANSACTIONS OF 10000 ROWS;
