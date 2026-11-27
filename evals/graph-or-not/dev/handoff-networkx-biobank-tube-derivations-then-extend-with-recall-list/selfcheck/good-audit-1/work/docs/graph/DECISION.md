# Recall list: where the tube walk lives

Decision: in-process-library

## Workload facts (from the conversation of 2026-11-24)

- 18,400 tubes, 21,900 derivation rows (nightly export from LIMS A and B), chains up to 6 steps; a few recalls a month.
- **Ids:** 212 ids differ only by case or a trailing space (LIMS B exports lower case). The lab confirmed: same tube.
  Normalise (strip, upper-case) before building the graph.
- **Recall rule (lab manager):** every tube derived from the recalled one, any number of steps. Destroyed tubes are
  left off the list, but tubes made from them are on it (walk through them).

## Options considered

- graph-database (Priya): rejected, a server for a few queries a month.
- in-process-library: chosen; networkx is already a dependency. Do not reuse tubetrack/graph.py as is: it adds raw ids.
- recursive-sql: there is no SQL database here.

## What would change the decision

- Recalls needed interactively across many sites, or an export too large to load.
