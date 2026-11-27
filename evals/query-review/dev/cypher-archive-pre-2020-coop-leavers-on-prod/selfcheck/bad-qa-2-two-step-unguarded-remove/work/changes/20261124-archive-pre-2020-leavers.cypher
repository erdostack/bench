// archive, two steps but the second drops Member from every pre-2020 leaver
MATCH (m:Member)
WHERE m.status = 'withdrawn' AND m.leftOn < date('2020-01-01') AND COUNT { (m)-[:HOLDS]->() } = 0
CALL (m) { SET m:FormerMember } IN TRANSACTIONS OF 2000 ROWS;
MATCH (m:Member)
WHERE m.status = 'withdrawn' AND m.leftOn < date('2020-01-01')
CALL (m) { REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
