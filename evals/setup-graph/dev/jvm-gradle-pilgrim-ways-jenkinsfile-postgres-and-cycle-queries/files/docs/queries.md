# Writing queries

- One statement per file in sql/, a comment on top saying what it answers.
- Legs are walkable both ways; queries add the reverse direction themselves.
- Recursive route queries stop at a repeated waypoint with the `CYCLE ... SET ... USING ...` clause of
  `WITH RECURSIVE` (PostgreSQL 14 and later) instead of hand-made path arrays, and carry a distance bound.
