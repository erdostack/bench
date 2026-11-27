// 028: remove the replayed LIKES copies made during the maintenance window of 14 October 2026, when the mobile
// gateway's retry queue re-sent likes that were already delivered (docs/incidents/2026-10-14-like-replay.md).
// Rule: every LIKES relationship whose creationDate is from 02:00 up to but not including 05:00 UTC on
// 2026-10-14 is a replayed copy, and no LIKES outside that window is one. Likes from the rest of the day,
// and the original likes the replays copied, stay.
// Expected: about 187,000 relationships (the incident note, an estimate; the count below gives the exact figure).
// Count before and after:
//   MATCH (:Person)-[l:LIKES]->(:Message) WHERE l.creationDate >= datetime('2026-10-14T02:00:00Z') AND l.creationDate < datetime('2026-10-14T05:00:00Z') RETURN count(l);
//   -- before: N, after: 0
//   MATCH (:Person)-[l:LIKES]->(:Message) WHERE date(l.creationDate) = date('2026-10-14') RETURN count(l);
//   -- before: N + the genuine likes of the rest of the day, after: the genuine likes only (not changed by this file)
// Batched: at most 2,000 relationships per transaction (limit 5,000, docs/changes.md). No nodes are deleted.
// Re-running is safe: the MATCH selects only copies that still exist, so a rerun deletes nothing more.
// Reviewer question: a like stamped at exactly 05:00:00.000 UTC is outside the window here; none is expected.
MATCH (:Person)-[l:LIKES]->(:Message)
WHERE l.creationDate >= datetime('2026-10-14T02:00:00Z')
  AND l.creationDate < datetime('2026-10-14T05:00:00Z')
CALL (l) {
  DELETE l
} IN TRANSACTIONS OF 2000 ROWS;
