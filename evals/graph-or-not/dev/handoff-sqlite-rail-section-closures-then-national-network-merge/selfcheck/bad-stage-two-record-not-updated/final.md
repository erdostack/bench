Decision: in-process-library

The call was to keep the recursive query because it ran at 120 ms p95 against the desk's 1 s budget on about
9,800 sections. On the merged network it is 7.4 s, more than seven times over, and the plan is already index
lookups. More cores will not help: SQLite runs one query on one core. Load the nightly export into networkx once a
night instead: 380,000 sections is a few hundred MB on the 8 GB box, and the cut-off walk takes a fraction of a
second.
