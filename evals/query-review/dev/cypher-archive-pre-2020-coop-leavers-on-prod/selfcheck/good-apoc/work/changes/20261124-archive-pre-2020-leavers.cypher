// 20261124: archive withdrawn members who left before 2020 and have no HOLDS left.
CALL apoc.periodic.iterate(
  "MATCH (m:Member) WHERE m.status = 'withdrawn' AND m.leftOn < date('2020-01-01') AND NOT (m)-[:HOLDS]->() RETURN m",
  "SET m:FormerMember REMOVE m:Member",
  {batchSize: 1000}
);
