# Headcount rollup over the unit tree

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-24)

- About 1,900 units, at most 8 levels; 23,000 people; the pack runs monthly plus ad-hoc reruns.

## Options considered

- graph-database (Ines): rejected; a second store for a monthly rollup.
- in-process-library: would work at this size; nothing to gain.
- recursive-sql: chosen. A recursive query from each unit to its descendants, summed.

## What would change the decision

- Interactive what-if re-organisations over the whole tree.
