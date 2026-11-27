Rerunning it as is would double the first half: last night committed 21 batches (10,500 meetings, through
2025-05-29) before the kill, meetings has no unique key, and the ranking counts every row (docs/ranking.md).
Resuming from the logged date doesn't work either: the last batch stopped part-way through 2025-05-29
(5 of that day's 17 matches are in), so `> '2025-05-29'` skips 12 and `>=` doubles 5.

jobs/backfill_meetings.py now inserts, 500 at a time, only played matches that have no meetings row yet
(with an index on meetings.match_id so the check is cheap). On the copy it adds the remaining 10,968 and
ends with exactly one row per played match; killed and restarted it picks up where it stopped. Check:
`SELECT count(*), count(DISTINCT match_id) FROM meetings` should match the played-match count.
