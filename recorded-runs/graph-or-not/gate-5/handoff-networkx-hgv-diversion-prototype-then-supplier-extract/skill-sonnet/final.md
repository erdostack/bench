Decision: in-process-library

The regional extract settles the missing fact. The earlier record said need-more-information only because the extract size was unknown.

- Your pilot figures are 70 MB for 38,000 segments, which is about 1,842 B per segment. At 180,000 segments that comes to about 332 MB, roughly 22% of the 1.5 GB worker limit.
- A route took 30 ms in the pilot. Scaled linearly to the extract it is about 142 ms at most, against the 2 s budget. At 300 checks a day, checks almost never overlap.
- A graph database, which Dan proposed, is not justified at this size. Recursive SQL is the wrong tool for a weighted shortest path with a weight limit.
- The prototype in `roads/diversion.py` can keep running as it is. Its closed-segment lookup scans every edge on each call. Indexing segment_id to its junctions at load time would remove that scan. I did not make that change.

Caveats:
- Everything here is arithmetic from your numbers, not a measurement. The extract and `var/roads.db` are not in the repo, so I ran nothing.
- Before release, measure worker memory after `load(conn)` and a route time on the delivered extract. The 150,000 junctions on 180,000 segments is a high junction ratio, and I don't know the pilot's ratio, so memory could come out above 332 MB.
- The national product (about 4 million segments, about 7.4 GB in this structure) would not fit in a worker. That would reopen the decision.

I updated `docs/graph/DECISION.md` with the new facts, the decision and the conditions that would change it. I changed no code.
