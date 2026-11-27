// 20261124: archive members who withdrew before 2020 (the AGM mailing still pulls them in): replace the
// Member label with FormerMember. Members still being repaid keep HOLDS and stay Members (docs/model.md).
// At most 2,000 nodes per transaction. Count first:
// MATCH (m:Member) WHERE m.status IN ['withdrawn', 'deceased'] AND m.leftOn < date('2020-01-01') AND NOT (m)-[:HOLDS]->() RETURN count(m);
MATCH (m:Member)
WHERE m.status IN ['withdrawn', 'deceased'] AND m.leftOn < date('2020-01-01') AND NOT EXISTS { (m)-[:HOLDS]->(:Site) }
CALL (m) {
  SET m:FormerMember
  REMOVE m:Member
} IN TRANSACTIONS OF 2000 ROWS;
