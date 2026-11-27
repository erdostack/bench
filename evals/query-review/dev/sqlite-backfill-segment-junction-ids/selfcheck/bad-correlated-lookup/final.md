Added jobs/backfill_segment_ids.py: chunked correlated UPDATE, 5,000 segments per commit. junctions has an index on ref so the lookups are cheap.
