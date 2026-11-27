MATCH (j:Job)
WHERE NOT (j)<-[:OWNS]-(:Team)
RETURN j.name AS job, j.schedule AS schedule
ORDER BY job
