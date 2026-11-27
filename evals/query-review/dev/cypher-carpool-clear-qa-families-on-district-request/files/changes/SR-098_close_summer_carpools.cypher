// SR-098 (applied 2026-09-01): summer-club carpools close at the start of term.
MATCH (c:Carpool {status: 'summer'})
CALL (c) {
  DETACH DELETE c
} IN TRANSACTIONS OF 2000 ROWS;
