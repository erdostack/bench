// ticket: AGM Oct 2026 retention decision (docs/retention.md): keep plays from 2024-01-01 on. DRAFT, needs PR review before the tech rota runs it.
// Batched: a play has at most 7 relationships, so at most 8 entities deleted per play; 600 plays * 8 = 4,800 <= 5,000 per transaction.
// Tracks, shows, presenters and Return nodes are untouched; only the plays and their relationships go.
// Pre-check (read only): MATCH (p:Play) WHERE p.airedOn < date('2024-01-01') RETURN count(*);  // expect about 612,000 (2026-11-20)
MATCH (p:Play)
WHERE p.airedOn < date('2024-01-01')
CALL {
  WITH p
  DETACH DELETE p
} IN TRANSACTIONS OF 600 ROWS;
