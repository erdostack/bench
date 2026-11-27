# Conflict-of-interest filter in the reviewer picker

Decision: no-graph

## Workload facts (given by the owner, 2026-11-23)

- Rule (editor-in-chief, explicit): a conflict is having co-authored a paper with any of the submission's authors
  in the last 24 months. Direct co-authors only, not co-authors of co-authors. Institutions do not count.
- 310k researchers, 1.4M papers, 5.2M authorship rows, all in Postgres.
- About 1,800 submissions a month; the picker should open in under a second.

## Options considered

- graph-database (Bram's proposal): rejected. A second store, loaded weekly, for a one-step lookup.
- in-process-library: rejected. Holding the co-authorship network in the app to read one ring of it.
- recursive-sql: not needed. Nothing recurses; the rule stops at direct co-authors.
- no-graph: chosen. One join: submission authors -> their papers in the window -> the papers' other authors.

## What would change the decision

- The rule reaching further than direct co-authors (co-authors of co-authors), or a requirement to rank by
  collaboration distance.
