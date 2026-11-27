Decision: recursive-sql

No change is needed. `sql/cut_off.sql` is a recursive walk over the nightly SQLite export, and at your stated 120 ms p95 it answers well inside the 1 s budget for about 30 closures a day. Ravi's graph database would add a second server on the same 8 GB box, fed from the nightly export, to answer a question that already fits.

Numbers the decision turns on:
- Present p95: 120 ms (your figure; the repo holds no timing and no `var/infra.db`).
- Budget headroom: about 8 times (1 s against 120 ms).
- My synthetic check at 640 stations and 9,800 sections, with the track node count unknown: p95 116 ms at 3,000 nodes and 320 ms at 8,000 nodes. Both are under 1 s.
- Load: 30 closures a day x 120 ms is about 3.6 s of query time per day.

What I could not find or measure: the real track node count and core node count, the real topology (my check used random graphs), the plan on the real file, and the owner of the 1 s budget. The margin depends on the node count, so re-run the query on the real file before a tender.

What would change this: a real p95 above 1 s (check the plan and indexes first, then consider an in-process copy rebuilt after each nightly export), many closures overlapping at peak, or a need for the network as it is during the day rather than last night's export.

Nothing in the repo was changed. The decision record is at `docs/graph/DECISION.md`, and the synthetic benchmark folder was removed.
