Added jobs/backfill_depth.py: it walks posts in id ranges of 2,000 (a reply is always newer than its
parent, so the parent's depth is already set) and commits per range. It filled 60,000 rows on the copy.
