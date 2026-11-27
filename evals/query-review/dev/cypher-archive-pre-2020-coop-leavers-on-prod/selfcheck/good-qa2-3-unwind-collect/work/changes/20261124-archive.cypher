// archive members who withdrew before 2020 and hold no shares
UNWIND ['withdrawn'] AS st
MATCH (m:Member {status: st}) WHERE m.leftOn < date({year: 2020, month: 1, day: 1}) AND NOT EXISTS { (m)-[:HOLDS]-() }
WITH collect(m) AS ms
UNWIND ms AS m
CALL (m) { SET m:FormerMember REMOVE m:Member } IN TRANSACTIONS OF 1000 ROWS;
