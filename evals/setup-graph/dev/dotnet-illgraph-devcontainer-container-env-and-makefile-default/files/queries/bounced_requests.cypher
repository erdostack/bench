// Requests routed through more than two branches before they were filled.
MATCH (r:Request)-[v:ROUTED_VIA]->(:Branch)
WITH r, count(v) AS steps
WHERE steps > 2
RETURN r.id, steps
ORDER BY steps DESC;
