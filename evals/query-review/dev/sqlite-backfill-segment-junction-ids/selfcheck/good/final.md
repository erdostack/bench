Added jobs/backfill_segment_ids.py. Before running anything I looked at the plan of the obvious
correlated UPDATE: the index on junctions.ref is COLLATE NOCASE and ref is a BINARY column, so
`ref = segments.from_ref` cannot use it and each lookup scans all 40,000 junctions (85,975 segments x 2
columns, billions of rows). The job instead loads ref -> id once and updates segments in id chunks of
5,000 with a commit per chunk. On the copy it filled 85,975 segments in a couple of seconds; every ref
resolved.
