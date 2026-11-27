# Ultimate exposure roll-up

Decision: graph-database

## Workload facts (from the owner, 2026-11-23)

- 3,400 contracts, 190 reinsurers, 21,000 cession rows; chains up to 9 deep.
- Spirals exist: 14 reinsurers retrocede back to themselves through others.
- exposure/rollup.sql multiplies shares along the chain and drops a branch below 0.1% of the original. No
  retrocession in the book passes on more than 60%, so every lap of a spiral shrinks the share and the walk ends
  (0.6^14 < 0.001).
- Runs in 40 s; the nightly window is 2 hours. Matched the actuaries' spreadsheet to the cent at 2025 year-end.

## Options considered

- graph-database (Ama's proposal): rejected. A second store for a batch that works; a graph query over spirals needs
  the same cut-off.
- in-process-library: would work at 21,000 rows, but there is nothing to fix.
- recursive-sql: chosen. Keep the query as it is.
- no-graph: no; it is a walk down chains.

## What would change the decision

- A retrocession passing on more than 60% (or 100%): the cut-off would no longer bound the laps; check the guard.
- Run time approaching the 2 hour window.
