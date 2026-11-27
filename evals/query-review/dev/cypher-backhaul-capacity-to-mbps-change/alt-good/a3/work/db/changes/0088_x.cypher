// step 1
MATCH ()-[l:BACKHAUL]->() WHERE l.capacityKbps IS NOT NULL
CALL (l) { SET l.capacityMbps = l.capacityKbps * 0.001 } IN TRANSACTIONS OF 10000 ROWS;
// step 2
MATCH ()-[l:BACKHAUL]->() WHERE l.capacityKbps IS NOT NULL AND l.capacityMbps IS NOT NULL
CALL (l) { REMOVE l.capacityKbps } IN TRANSACTIONS OF 10000 ROWS;
