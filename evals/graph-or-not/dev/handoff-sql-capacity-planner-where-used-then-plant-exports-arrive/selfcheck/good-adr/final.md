Decision: in-process-library

Old vs new:

- memory: allowed 2 GB extra for the planner; needed 1.4 GB for all three plants.
- run time: must be under 10 minutes; networkx did all 40,000 where-used lookups in 3 minutes, while the
  per-component query was 90 ms each, about an hour, on Linz alone.

Both records now say in-process-library.
