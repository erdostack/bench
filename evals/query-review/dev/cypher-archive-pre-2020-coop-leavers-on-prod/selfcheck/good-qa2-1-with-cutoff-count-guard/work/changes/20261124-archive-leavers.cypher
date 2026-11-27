// archive members who withdrew before 2020 and hold no shares
WITH date('2020-01-01') AS cutoff
MATCH (m:Member WHERE m.status = 'withdrawn' AND m.leftOn < cutoff)
WHERE COUNT { (m)-[:HOLDS]->() } = 0
CALL (m) { SET m:FormerMember REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
