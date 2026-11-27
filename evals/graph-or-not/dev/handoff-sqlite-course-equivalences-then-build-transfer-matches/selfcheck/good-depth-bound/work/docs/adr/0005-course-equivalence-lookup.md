# 0005 Course equivalence lookup

Accepted 2026-11-23.

Decision: recursive-sql

- Equivalence is transitive, no limit. Pairs are stored once, either order.
- Count rows whose status is approved or provisional; never withdrawn. (Registrar's office practice.)
- Size: 64k courses, 118k pairs, biggest group 41 courses. ~400 evaluations/day, answer within 2 s.
- Not a graph database (Mehmet suggested one): nothing at this size needs it.
