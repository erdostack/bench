// Net rides per day leaving each dock.
MATCH (d:Dock)
OPTIONAL MATCH (d)-[o:RIDES_TO]->()
WITH d, coalesce(sum(o.per_day), 0) AS out
OPTIONAL MATCH ()-[i:RIDES_TO]->(d)
RETURN d.id, out - coalesce(sum(i.per_day), 0) AS net ORDER BY net DESC;
