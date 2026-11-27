MATCH (o:Object)
WHERE o.accessionYear = $year
RETURN o.objectId AS objectId, o.title AS title
ORDER BY o.accessionNumber
LIMIT 200;
