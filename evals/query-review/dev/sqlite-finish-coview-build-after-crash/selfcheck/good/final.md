What happened: the job adds a chunk's pairs in one transaction and saves progress in a second. Last night the
pairs for visits 18201-18300 committed, then the progress update failed (database is locked), so progress says
18200 but co_view already counts that chunk. Rerunning as is would add it twice.

`jobs/build_coviews.py` now (1) writes the pairs and the progress row in the same transaction, so a crash can't
split them again, and (2) has a one-off guard: if progress is still at 18200 it moves it to 18300 first instead
of re-adding that chunk. It returns the number of visits it processed (21,700 tonight). I didn't touch
var/gallery.db.
