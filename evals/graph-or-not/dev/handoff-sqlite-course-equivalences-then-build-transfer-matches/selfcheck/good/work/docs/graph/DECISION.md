# Transfer credit: equivalent courses

Decision: recursive-sql

## Workload facts (given by the owner, 2026-11-23)

- course_equivalence: 118k rows, one per pair, stored in either order. 64k courses.
- The registrar: equivalence is transitive with no limit (A = B and B = C gives A = C).
- Status: approved and provisional rows count the same (provisional until the department reviews it);
  withdrawn rows never count.
- The largest known group of mutually equivalent courses is 41.
- About 400 evaluations a day; the advisor screen should answer within 2 s.

## Options considered

- graph-database (Mehmet's proposal): rejected. A second store to keep in sync, for a walk over at most 41 courses.
- in-process-library: workable at this size, not needed.
- recursive-sql: chosen. One recursive query; pairs read both ways; the walk carries the courses it has visited.
- no-graph: rejected. Equivalence is transitive with no limit.

## What would change the decision

- Groups growing far past 41 courses, or the screen missing 2 s.
