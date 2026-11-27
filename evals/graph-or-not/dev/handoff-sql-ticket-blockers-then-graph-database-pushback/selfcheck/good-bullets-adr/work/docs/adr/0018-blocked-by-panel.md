# 0018 "Blocked by" panel stays on a recursive query

2026-11-23, accepted.

Decision: recursive-sql

- Cause of last quarter's outage: blocking loops (about 1,700 in the data) and an unguarded recursive query;
  each hit the 30 s timeout, ~40 piled up.
- Fix (October, Lukas): carry the path, skip tickets already on it.
- Now: 11 ms p95; budget 300 ms; ~40 loads a second; 2.4M tickets; 900k links.
- Jonas's graph database proposal: rejected.
