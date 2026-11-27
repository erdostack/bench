// Wagons the allocation screen offers for a flow: fleet wagons of the right type not allocated elsewhere.
MATCH (w:Wagon {type: $type})
WHERE w.status = 'active' AND NOT (w)-[:ALLOCATED_TO]->(:Flow)
RETURN w.wagonNo AS wagon
ORDER BY wagon
LIMIT 200;
