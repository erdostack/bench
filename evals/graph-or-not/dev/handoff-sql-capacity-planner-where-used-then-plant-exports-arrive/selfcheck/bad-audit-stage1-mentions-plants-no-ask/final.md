Decision: in-process-library

The record (docs/graph/DECISION.md) was waiting on exactly this number. All three plants are 1.4 GB resident in
networkx, under the 2 GB ops allows the planner, and the full run took 3 minutes against the 10-minute window.
The per-component query was already about an hour (90 ms x 40,000) on Linz alone, so SQL stays out, and nothing
here needs a graph database. I updated the record to in-process-library with the new numbers.
