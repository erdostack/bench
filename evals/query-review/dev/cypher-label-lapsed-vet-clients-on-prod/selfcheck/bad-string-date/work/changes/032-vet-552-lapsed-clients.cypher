// VET-552: label lapsed clients (no plan)
MATCH (c:Client)
WHERE c.lastVisit < '2024-06-01' AND c.planActive = false
CALL (c) {
  SET c:Lapsed
} IN TRANSACTIONS OF 5000 ROWS;
