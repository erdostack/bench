Decision: in-process-library

The currency graph is tiny: 160 nodes and about 4,600 directed edges, replaced every 10 seconds. Keep it in the
checkout process and search it there. Written up in docs/graph/DECISION.md.

- Treasury's rules bound the search: at most three conversions (two intermediates), best rate for the customer, and
  never through a restricted currency. Enumerating routes of up to three legs over a graph this size is well under a
  millisecond, inside the 15 ms at 300 conversions a second.
- A graph database would sit behind a network hop, or on every pod, for a few hundred kilobytes of data that is
  stale after 10 seconds anyway.
- recursive-sql on the local SQLite cache would also work for three steps; I'd keep the rate maths in code.
