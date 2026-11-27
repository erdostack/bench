MATCH (o:Object)
WHERE o.accessionYear IS NULL
SET o.accessionYear = toInteger(split(o.accessionNumber, '.')[0]);
