# Batch lead time on the planning screen

Decision: in-process-library

## Workload facts (from the planning conversation, 2026-11-24)

- 1,800 recipes, about 26 steps each, in the SQLite file the bakers edit; step_dep says which steps wait on which.
- About 9% of steps are untimed. **Production manager's rule: an untimed step (minutes NULL) counts as 20
  minutes** until somebody times it.
- About 150 screen opens a morning, around 400 products each time.

## Options considered

- graph-database (Jonas): rejected, a server for a few thousand graphs of 26 nodes.
- in-process-library: chosen. networkx is already installed; longest path per recipe, read fresh from the file.
- recursive-sql: would also work on the file; networkx is simpler to read.
- no-graph: no, it is a longest path through the step graph.

## What would change the decision

- Resource constraints (one oven, two mixers) entering the lead time: that is scheduling, not a path.
