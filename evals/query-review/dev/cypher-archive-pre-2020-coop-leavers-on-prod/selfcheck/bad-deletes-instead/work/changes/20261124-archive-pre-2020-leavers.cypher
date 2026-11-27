// 20261124: remove pre-2020 leavers with no shares
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < date('2020-01-01') AND NOT (m)-[:HOLDS]->()
CALL (m) { DETACH DELETE m } IN TRANSACTIONS OF 500 ROWS;
