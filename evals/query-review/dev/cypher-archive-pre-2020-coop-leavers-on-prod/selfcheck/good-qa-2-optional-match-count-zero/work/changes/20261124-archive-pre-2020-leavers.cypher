// archive
MATCH (m:Member)
WHERE m.status = 'withdrawn' AND m.leftOn < date('2020-01-01')
OPTIONAL MATCH (m)-[h:HOLDS]->()
WITH m, count(h) AS holdings
WHERE holdings = 0
CALL (m) {
  SET m:FormerMember
  REMOVE m:Member
} IN TRANSACTIONS OF 500 ROWS;
