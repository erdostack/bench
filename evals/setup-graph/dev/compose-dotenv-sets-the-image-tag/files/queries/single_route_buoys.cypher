// Buoys whose readings can leave through one neighbour only.
MATCH (b:Buoy)-[:RELAYS_TO]->(n)
WITH b, count(DISTINCT n) AS exits
WHERE exits = 1
RETURN b.code AS buoy
ORDER BY buoy;
