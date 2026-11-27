MATCH (:Site)-[l:BACKHAUL]->(:Site) WHERE l.capacityMbps IS NULL
CALL (l) { SET l.capacityMbps = toFloat(l.capacityKbps) / 1000 REMOVE l.capacityKbps } IN TRANSACTIONS OF 5000 ROWS;
