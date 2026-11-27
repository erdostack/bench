// ticket: FLEET-340 clear waitlist places that lapsed (since before 2026-05-01, six months back). Nodes, HOME, BOOKED untouched.
MATCH (:Member)-[w:WAITLISTED WHERE w.since < date('2026-05-01')]-(:Zone)
CALL (w) { DELETE w } IN TRANSACTIONS OF 1000 ROWS;
