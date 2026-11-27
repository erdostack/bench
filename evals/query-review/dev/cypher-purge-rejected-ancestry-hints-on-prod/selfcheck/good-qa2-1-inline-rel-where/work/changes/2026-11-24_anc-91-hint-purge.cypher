// ticket: ANC-91 hint purge: rejected hints created before 2026-08-01 without a researchRef (docs/hints.md). Count before/after with count(h); EXPLAIN first.
MATCH (:Person)-[h:HINT WHERE h.status = 'rejected' AND h.createdAt < datetime('2026-08-01T00:00:00Z') AND h.researchRef IS NULL]->(:Person)
CALL (h) { DELETE h } IN TRANSACTIONS OF 10000 ROWS;
