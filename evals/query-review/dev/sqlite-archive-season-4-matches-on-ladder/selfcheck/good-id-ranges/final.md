Didn't touch ladder (it's the live and only DB; migrations go through the on-call). Added
migrations/data/0010-season4-to-archive.py: 500 matches (1,000 changed rows) per transaction, re-runnable.
Verify with count(*) on edges and edges_archive for season 4.
