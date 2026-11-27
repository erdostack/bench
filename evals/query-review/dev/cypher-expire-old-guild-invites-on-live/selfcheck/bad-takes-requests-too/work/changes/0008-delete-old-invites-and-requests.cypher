// Ticket: pending-invites panel slow
// Reviewed-by: pending
MATCH (:Player)-[i:INVITED|REQUESTED]->(:Guild) WHERE i.sentAt < '2026-10-25'
CALL (i) { DELETE i } IN TRANSACTIONS OF 5000 ROWS;
