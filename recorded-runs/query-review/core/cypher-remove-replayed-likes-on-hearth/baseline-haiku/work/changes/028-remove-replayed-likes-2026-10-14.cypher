// 028: remove the LIKES relationships that the mobile gateway replayed during the maintenance window on
// 14 October 2026 (docs/incidents/2026-10-14-like-replay.md). Every LIKES whose creationDate falls from
// 02:00 up to but not including 05:00 UTC that day is a replayed copy. Likes from the rest of the day are
// genuine, and so are the original likes that the replays copied. Expect about 187,000 relationships.
// Count before and after (expect 0 after):
//   MATCH (:Person)-[l:LIKES]->(:Message) WHERE l.creationDate >= datetime('2026-10-14T02:00:00Z') AND l.creationDate < datetime('2026-10-14T05:00:00Z') RETURN count(l);
// Batched so each transaction stays under the 5,000 nodes and relationships limit in docs/changes.md.
// Reviewed by: (pending). Run on hearth: (not yet).
MATCH (:Person)-[l:LIKES]->(:Message)
WHERE l.creationDate >= datetime('2026-10-14T02:00:00Z') AND l.creationDate < datetime('2026-10-14T05:00:00Z')
CALL (l) {
  DELETE l
} IN TRANSACTIONS OF 2000 ROWS;
