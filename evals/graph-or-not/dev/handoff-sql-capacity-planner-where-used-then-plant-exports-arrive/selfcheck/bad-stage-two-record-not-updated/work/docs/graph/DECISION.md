# Capacity planning run: where the where-used lives

Decision: need-more-information

## Workload facts (from the conversation of 2026-11-24)

- A run re-plans about 40,000 changed components and needs the full where-used of each (any depth).
- sql/where_used.sql per component: 90 ms on Linz data (180,000 BOM lines), so a run is about an hour.
- **The run must finish within 10 minutes** (shift handover).
- **Ops allows the planner service 2 GB more memory on its hosts, no more.**
- From next quarter the run covers Brno and Pune too; their sizes are unknown.

## Options considered

- recursive-sql (today): out, an hour against 10 minutes on a sixth or less of the data.
- in-process-library: the candidate if all three plants fit in 2 GB inside the planner.
- graph-database (Kai): only if they do not fit.
- no-graph: no, the where-used goes up any number of levels.

## What would change the decision / what is missing

- The Brno and Pune BOM line counts, and the resident size of all three plants loaded into networkx.
