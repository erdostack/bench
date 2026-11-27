# Crash grouping

Decision: in-process-library

## Workload (stated 2026-11-23)

- Connected components of crash_report via crash_link over 7 days: about 4M reports, 11M links.
- Window: 1 hour before the triage stand-up. The SQL label-propagation job took 5 h 40 min last night.
- networkx on the same week from a dump: 9 minutes, 19 GB peak; the batch box has 64 GB, idle at night.
- Team: Python; nobody wants another server.

## Options

- graph-database: rejected; a server to load every night for one components pass.
- in-process-library: chosen.
- recursive-sql: rejected; the in-database route is the one measured at 5 h 40 min.
- no-graph: rejected; chains of links make it transitive.

## What would change this

- The week's graph outgrowing the box (19 GB of 64 GB today).
