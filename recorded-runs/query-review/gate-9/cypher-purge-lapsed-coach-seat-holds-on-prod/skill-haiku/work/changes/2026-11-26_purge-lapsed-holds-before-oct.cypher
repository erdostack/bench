// ticket: HOL-58 purge lapsed seat holds created before 2026-10-01, except holds with a depositRef (docs/holds.md: the refund is reconciled against the hold, so such a hold is never purged). Deletes HOLDS relationships only; customers, departures, bookings and coaches are untouched. Batches of 10,000 rows keep each transaction under the 25,000-row limit (docs/environments.md).
MATCH (:Customer)-[h:HOLDS]->(:Departure)
WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL
CALL (h) {
  DELETE h
} IN TRANSACTIONS OF 10000 ROWS;
