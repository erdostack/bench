// 20261125 archive pre-2020 leavers with no shares left
MATCH (m:Member)
WHERE m.status = 'withdrawn' AND m.leftOn.year < 2020 AND COUNT { (m)-[:HOLDS]->() } = 0
CALL { WITH m SET m:FormerMember REMOVE m:Member } IN TRANSACTIONS OF 500 ROWS;
