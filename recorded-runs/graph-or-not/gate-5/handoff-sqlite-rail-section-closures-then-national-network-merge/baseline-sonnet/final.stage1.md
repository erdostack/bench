Decision: recursive-sql

No change needed. The query already is the right tool, and it is well inside the requirement.

- **Performance:** 120 ms p95 against a 1 s requirement leaves about 8 times of headroom. About 30 closures a day is negligible load.
- **Scale:** 640 stations and about 9,800 sections is small. The whole network fits in memory many times over on an 8 GB box, and SQLite handles it without effort.
- **Query shape:** `sql/cut_off.sql` is a plain reachability walk from the core nodes. It uses `UNION` and carries only `node_id`, so a node that is reached again is dropped. That makes it safe on loops, and it terminates. Both directions of a section are used, matching the schema ("usable in both directions"), and `section_a` and `section_b` index the join.
- **Operations:** the register is exported nightly into `var/infra.db`. A graph database would add a second datastore, a load step after every export, and something new to run and secure. An in-memory graph library would add a dependency and a copy of the data to keep fresh. Neither buys anything at this size. Ravi's case for a graph database would need a different kind of question, not this one.

I read the query, the schema and the desk script. I haven't run anything, so the 120 ms figure is yours and I haven't re-measured it.

What would make me reconsider:
- The latency requirement falls well below the current figure, or the network grows by a couple of orders of magnitude.
- The desk starts asking questions that go beyond reachability, such as best re-routes, timetable-aware paths or shortest detours.
- Closures stop being single sections, for example if the desk wants to close several at once. The query would need a list parameter, which is still a small change in SQL.

One edge case to be aware of, not a reason to change tools. The final `NOT EXISTS` reports a station as cut off if it has no track nodes at all, because the join finds nothing reachable. If the export can contain such stations, they will always appear in the cut-off list, whichever section is closed. A quick check on the nightly export would tell you whether it happens.
