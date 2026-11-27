Decision: recursive-sql

A walk of at most 6 levels up parent_id over 14,000 rows in SQLite. One recursive query per org (or one for all of
them in the monthly run) is plenty; a graph database would be a second store for this. Written up with Finance's
rules in docs/graph/DECISION.md.

- Finance: the invoice goes to the highest org above it, or the org itself, that has its own billing account; if
  none in the chain has one, to the org itself.
- Foreign keys are not enforced (no PRAGMA) and 412 orgs point at a deleted parent. Finance: the chain ends at the
  last org that exists. A recursive query that joins org on parent_id does that naturally; a Python loop must not
  assume the parent row is there.
