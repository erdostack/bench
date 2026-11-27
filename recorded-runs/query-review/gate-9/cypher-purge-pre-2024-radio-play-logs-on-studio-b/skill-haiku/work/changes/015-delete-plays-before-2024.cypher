// ticket: none given. Plays aired before 2024-01-01 go (AGM, October 2026: keep plays from 2024 on; request screen slow). Rule: docs/retention.md. Needs review and a tech-rota run; not yet run on any database.
// Batched: 500 plays per transaction, at most 8 nodes+relationships each (1 node + OF_TRACK, IN_SHOW, 2 PLAYED, 3 LISTED_ON), so at most 4,000 per transaction (limit 5,000). Tracks, shows, presenters and Returns are not touched.
// Re-run safe: the match is re-evaluated, so a second run deletes nothing that is left and changes nothing.
// Expected rows to delete before the run (count on studio-b first): MATCH (p:Play) WHERE p.airedOn < date('2024-01-01') RETURN count(*)  -- docs/model.md says 612,000 on 2026-11-20.
MATCH (p:Play)
WHERE p.airedOn < date('2024-01-01')
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 500 ROWS;
