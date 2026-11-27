// archive, step 1 add label, step 2 drop Member
MATCH (m:Member)
WHERE m.status = 'withdrawn' AND m.leftOn < date('2020-01-01') AND COUNT { (m)-[:HOLDS]->() } = 0
CALL (m) { SET m:FormerMember } IN TRANSACTIONS OF 2000 ROWS;
MATCH (m:Member:FormerMember)
CALL (m) { REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
