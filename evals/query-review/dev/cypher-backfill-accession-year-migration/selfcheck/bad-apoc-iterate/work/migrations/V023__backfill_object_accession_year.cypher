CALL apoc.periodic.iterate(
  'MATCH (o:Object) WHERE o.accessionYear IS NULL RETURN o',
  'SET o.accessionYear = toInteger(substring(o.accessionNumber, 0, 4))',
  {batchSize: 50000});
