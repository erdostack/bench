// ticket: FLEET-340 clear waitlist places that lapsed (since before 2026-05-01, six months back). Nodes, HOME, BOOKED untouched.
MATCH (m:Member)
CALL (m) {
  MATCH (m)-[w:WAITLISTED]->(:Zone) WHERE w.since < date('2026-05-01')
  DELETE w
} IN TRANSACTIONS OF 1600 ROWS;
