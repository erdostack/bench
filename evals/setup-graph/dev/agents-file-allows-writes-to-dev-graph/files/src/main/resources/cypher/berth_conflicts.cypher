// Days on which more voyages arrive at a port than it has berths.
MATCH (v:Voyage)-[:TO]->(p:Port), (:Ship)-[s:SAILS]->(v)
WITH p, s.departs + duration({days: 2}) AS arrives, count(v) AS arrivals
WHERE arrivals > p.berths
RETURN p.code AS port, arrives, arrivals, p.berths AS berths
ORDER BY arrives;
