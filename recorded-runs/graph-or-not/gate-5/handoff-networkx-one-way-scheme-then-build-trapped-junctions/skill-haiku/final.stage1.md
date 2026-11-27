Decision: recursive-sql

The trapped-junctions check is a reachability question on one draft's road network. It does not need a graph database. Two recursive queries on the draft file (one from the ring road forward, one backward) and a set difference answer it in about 10 ms per draft, once the file has indexes on the segment endpoints.

- The graph is small: about 1,450 junctions and 1,900 segments, 40 to 60 drafts a week across both planners, so the whole week's checking is under a second of database time.
- The current script has three faults that the fix must remove. It gives up after 25 steps (`MAX_STEPS`), so the long market loop reads as trapped. It counts footpaths as roads. It checks only the direction to the ring road, not the direction from it. It also reports junctions that have only footpaths, which the rule excludes.
- The consultant's graph database would add a second store to two laptops and would have to be kept in step with the sketch tool's export, for no measured gain.

Before the fix is accepted, run it on last week's real draft and compare its output with the 63 flagged junctions one by one. My timings come from synthetic drafts that flag far more junctions than the real one, so the real file is the check that counts.

The full evidence, the options considered and what would change the decision are in `docs/graph/DECISION.md` in the working directory. Nothing else in the repo was changed.
