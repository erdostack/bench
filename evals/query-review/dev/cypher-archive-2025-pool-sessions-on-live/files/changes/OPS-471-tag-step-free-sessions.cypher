// OPS-471: tag every session in a pool with a hoist as :StepFree for the booking app's accessibility filter.
// Pools with a hoist: EAST and NORTH. About 37,000 sessions.
// Count before and after: MATCH (s:Session:StepFree) RETURN count(s);
// Reviewed by d.okafor, run on live 2026-06-02 by the duty systems officer.
MATCH (s:Session)-[:IN_POOL]->(p:Pool) WHERE p.code IN ['EAST', 'NORTH']
CALL (s) {
  SET s:StepFree
} IN TRANSACTIONS OF 5000 ROWS;
