Decision: in-process-library

The snapshot already is the graph, and the SDK walks it in memory in 0.08 ms. Recorded in docs/graph/DECISION.md.

- 640 flags and 1,100 prerequisite links, at most 4 deep, with loops rejected at save time: a few dictionary
  lookups per evaluation.
- The agreed limits are the real tripwire: snapshot under 5 MB (it is 1.2 MB) and evaluation under 1 ms p99. If one
  is crossed, the plan is server-side evaluation, not a graph database.
- A graph database would add a network hop to every flag check, or a second store behind a 1.2 MB JSON file.
