# Disruption desk: cut-off stations

Decision: recursive-sql

## Workload facts

- First conversation (2026-11-24): 640 stations, about 9,800 track sections; sql/cut_off.sql at 120 ms p95; the
  desk needs an answer within 1 s; about 30 closures a day; one box with 8 GB; register export rebuilt nightly.
  Decided then: recursive-sql (change nothing).
- April merge (2026-11-24): 2,600 stations, 380,000 track sections; replay 7.4 s p95 with indexes on both ends
  and index lookups in the plan.

## Options considered

- recursive-sql (keep, more cores, as Kofi suggests): rejected. 7.4 s against 1 s, and one SQLite query runs on
  one core, so more cores do not shorten it.
- in-process-library: chosen. Load the nightly export into networkx once a night: 380,000 sections is a few
  hundred MB on the 8 GB box, and a reachability walk from the core is well under a second.
- graph-database (Ravi): would work, but it is a server to sync nightly for 30 lookups a day.
- no-graph: no; it is reachability.

## What would change the decision

- Closures needed during the day on live track data, or the network outgrowing the box's 8 GB.
