Added a unique index on meetings.match_id and switched to INSERT OR IGNORE, so a rerun skips the 10,500 already in. Checked with count(*) vs count(DISTINCT match_id).
