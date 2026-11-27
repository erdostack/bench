# Query style

- We write Cypher 25. New queries use `LET` for intermediate values and `FILTER` instead of `WITH ... WHERE`
  when a step only filters.
- Every query file starts with a one-line comment saying what it answers.
- Parameters, never string concatenation; the runner passes `--param key=value` pairs.
- Bound variable-length patterns (`*1..6`, never bare `*`).
