MATCH ()-[l:BACKHAUL]->()
WHERE l.capacityKbps IS NOT NULL
SET l.capacityMbps = l.capacityKbps / 1000.0
REMOVE l.capacityKbps;
