// step 1: tag members who withdrew before 2020 and hold no shares
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < date('2020-01-01') AND NOT (m)-[:HOLDS]-()
CALL (m) { SET m:FormerMember } IN TRANSACTIONS OF 2000 ROWS;
