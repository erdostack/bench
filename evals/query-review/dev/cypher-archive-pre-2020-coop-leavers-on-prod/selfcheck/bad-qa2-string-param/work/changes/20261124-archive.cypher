// archive members who withdrew before 2020 and hold no shares
:param cutoff => '2020-01-01'
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < $cutoff AND NOT (m)-[:HOLDS]->()
CALL (m) { SET m:FormerMember REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
