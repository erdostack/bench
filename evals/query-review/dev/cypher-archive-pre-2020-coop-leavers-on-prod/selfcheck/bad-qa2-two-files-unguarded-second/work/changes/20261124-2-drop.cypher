// step 2: drop Member from withdrawn pre-2020 leavers
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < date('2020-01-01')
CALL (m) { REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
