// archive members who withdrew before 2020 and hold no shares
CALL apoc.periodic.iterate(
  "MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < $cutoff AND NOT (m)-[:HOLDS]->() RETURN m",
  "SET m:FormerMember REMOVE m:Member",
  {batchSize: 2000, params: {cutoff: '2020-01-01'}});
