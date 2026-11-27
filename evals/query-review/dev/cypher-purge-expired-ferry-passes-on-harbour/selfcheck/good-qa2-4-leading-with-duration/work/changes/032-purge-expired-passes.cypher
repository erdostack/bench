// 032: delete passes valid until before 2026-01-01 (about 38,000) with their relationships; customers, routes, sailings stay.
// Count before and after: MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
WITH date('2026-01-02') - duration({days: 1}) AS cutoff
MATCH (p:Pass) WHERE p.validUntil < cutoff
CALL (p) { DETACH DELETE p } IN TRANSACTIONS OF 24 ROWS;
