Decision: graph-database

Each of the cheaper options has been measured failing, and the workload matches the profile a dedicated graph store is for.

The numbers it turns on:
- Recursive SQL with the path array and both-end indexes: 8.4 s p95 against the 1.5 s budget, 5.6 times over. The closure table you tried (6.8 billion rows, invalidated by every switching operation) is a closed remedy.
- In-process library: 2.1 GB / 0.06 = 35 GB for the whole grid against 16 GB per trace server. The region split fails because 41% of storm traces cross regions.
- The data changes all day (about 45,000 device-state changes a day, 0.52 per second) and traces run online at about 0.25 per second in a storm, with a walk of data-dependent depth over 2.9M nodes and 3.4M segments.

This does not come free. You take on a second stateful system to operate, a feed from `netmodel` that can drift from the system of record, and a new query language. It also does not remove the meshed topology, so keep your loop handling. Before committing money, run a trial on the full network with last January's storm mix at 900 traces an hour and the switching feed applied, and require 1.5 s p95.

Two things I could not rule out because nobody has run them. The current query returns one row per route (`UNION ALL` plus a path array) and then applies `DISTINCT`, so some of the 8.4 s may be route repetition. An array-based in-memory layout would use far less than networkx's 35 GB. Neither reopens a rung that was measured failing, but each is a cheap thing to measure alongside the trial, and either passing would change the answer (recursive-sql or in-process-library).

I could not find: the PostgreSQL version, the number of trace servers, how many nodes a typical trace must reach, the share of storm traces that time out, or how stale a trace may be after switching. I measured nothing, since the repo has no database. I wrote `docs/graph/DECISION.md` with the facts and conditions. Nothing else in the repo was changed.
