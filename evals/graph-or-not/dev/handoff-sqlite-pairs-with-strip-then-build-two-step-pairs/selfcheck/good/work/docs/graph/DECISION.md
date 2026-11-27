# "Pairs with" strip

Decision: no-graph

## Workload (stated 2026-11-23, after a session with merchandising)

- Strip = products paired with this one, plus products paired with those. Two steps, never more: merch tried the
  three-step mock-up from docs/proposals/pairs-graph.md and rejected it.
- `pairing`: 180k rows over 40k products; a pair is stored once (product_a < product_b), so read both ways.
- Product pages peak at about 1,500/s; the strip has 30 ms of the page budget. Postgres.

## Options

- graph-database (the proposal): rejected; its reason was the three-step ranking, which merch do not want.
- in-process-library: rejected; a copy to keep in sync for two indexed joins.
- recursive-sql: not needed; the depth is fixed at two, so two joins say it more plainly.
- no-graph: chosen. Two joins on `pairing` in sql/pairs_with.sql.

## What would change this

- Merch asking for more steps or for ranking by paths; then revisit (recursive SQL first).
