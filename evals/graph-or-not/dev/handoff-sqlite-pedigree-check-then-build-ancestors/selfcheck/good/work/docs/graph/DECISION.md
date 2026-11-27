# Common-ancestor check: where does the pedigree walk live?

Decision: recursive-sql

## Workload facts (from the maintainer, 2026-11-23)

- Herd book: 6.4M animals in Postgres 15; each has `sire_id` and `dam_id`, NULL for founders. Both columns are indexed.
- The society's rule looks 4 generations back and no further. Fixed by the rule book.
- Deepest pedigree on record: 23 generations. Irrelevant to the check because of the 4-generation cap.
- About 900 matings a day; the check runs inside the web request and may take up to 1 second.
- Team: 2 backend developers, no graph database experience.

## Options considered

- graph-database (Matteo's Neo4j proposal): rejected. A second copy of 6.4M animals and a new system to run, to
  answer a question that reads at most 30 rows per animal.
- in-process-library: rejected. Would hold the herd book in memory to walk four steps.
- recursive-sql: chosen. One recursive query over `animal`, generation counter capped at 4, for sire and dam; the
  common ancestors are the intersection.
- no-graph: close. Four fixed self-joins would also work; the recursive form is shorter and gives the generation.

## What would change the decision

- The rule changing to an unbounded look-back together with whole-pedigree analytics (inbreeding coefficients over
  all 23 generations for every animal).
- The check failing its 1 second allowance on Postgres with the indexes in place.
