// archive members who withdrew before 2020 and hold no shares
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < date('2020-01-01')
OPTIONAL MATCH (m)-[h:HOLDS]->(:Site)
WITH m, count(h) AS held WHERE held = 0
CALL (m) { SET m:FormerMember } IN TRANSACTIONS OF 2000 ROWS
WITH m
CALL (m) { REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
