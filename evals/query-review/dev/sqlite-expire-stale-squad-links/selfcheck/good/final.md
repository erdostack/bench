Wrote jobs/expire_squad_links.py (2,000 pairs per commit, returns the count: 46,750 on the copy).
Heads-up: last_played is mixed. Console hosts report unix seconds and the sync service stores them as
integers (23,581 rows); everything else is ISO text. A plain `last_played < '2026-05-01'` would delete all
console pairs, including 10,482 that played recently, because SQLite sorts numbers before text. The job
compares integers against unixepoch('2026-05-01') and text against the date string.
