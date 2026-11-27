// 20261124: archive pre-2020 leavers
MATCH (m:Member {status: 'withdrawn'}) WHERE m.leftOn < date('2020-01-01') AND NOT (m)-[:HOLDS]->()
SET m:FormerMember REMOVE m:Member;
