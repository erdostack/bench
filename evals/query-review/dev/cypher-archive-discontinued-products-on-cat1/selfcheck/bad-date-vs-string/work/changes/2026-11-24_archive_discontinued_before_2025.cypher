// change: archive products discontinued before 2025-01-01 (add :Archived, remove :Live), 5,000 per transaction
MATCH (p:Product)
WHERE p.discontinuedOn < '2025-01-01'
CALL (p) {
  SET p:Archived
  REMOVE p:Live
} IN TRANSACTIONS OF 5000 ROWS;
