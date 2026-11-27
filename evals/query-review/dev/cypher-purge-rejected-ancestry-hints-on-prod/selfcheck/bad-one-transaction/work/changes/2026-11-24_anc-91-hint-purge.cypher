// ticket: ANC-91 hint purge: rejected hints created before 2026-08-01, except those with a researchRef
// (evidence in a research case, never purged: docs/hints.md). 10,000 per transaction (limit 20,000).
// Count before and after:
//   MATCH ()-[h:HINT]->() WHERE h.status = 'rejected' AND h.createdAt < datetime('2026-08-01T00:00:00Z')
//     AND h.researchRef IS NULL RETURN count(h);
MATCH (:Person)-[h:HINT]->(:Person)
WHERE h.status = 'rejected'
  AND h.createdAt < datetime('2026-08-01T00:00:00Z')
  AND h.researchRef IS NULL
DELETE h;
